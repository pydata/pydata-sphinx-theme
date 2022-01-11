""" use pa11y-ci to generate an accessibility report
"""
import json
import os
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen
from yaml import safe_dump

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent
BUILD = HERE / "_build"
PA11Y_BUILD = Path(os.environ.get("PA11Y_BUILD", BUILD / "pa11y"))
PA11Y_JSON = PA11Y_BUILD / "pa11y-ci-results.json"
PA11Y_ROADMAP = HERE / "a11y-roadmap.txt"
YARN = [shutil.which("yarn"), "--silent"]
SITEMAP = "http://127.0.0.1:8000/sitemap.xml"
REPORT_INDEX_URL = (PA11Y_BUILD / "index.html").as_uri()


def clean():
    if PA11Y_BUILD.exists():
        shutil.rmtree(PA11Y_BUILD)
    PA11Y_BUILD.mkdir(parents=True)


def serve():
    """start the local server"""
    server = subprocess.Popen(
        [sys.executable, HERE / "serve.py"],
    )
    ready = 0
    retries = 10
    while retries and not ready:
        retries -= 1
        try:
            time.sleep(1)
            ready = urlopen(SITEMAP)
        except URLError:
            pass

    assert ready, "server did not start in 10 seconds"

    return server


def audit():
    """run audit, generating a raw JSON report"""
    audit_rc = subprocess.call(
        f"yarn --silent pa11y-ci --json --sitemap {SITEMAP} > {PA11Y_JSON}",
        shell=True,
        cwd=ROOT,
    )

    return audit_rc


def report():
    """generate HTML report from raw JSON"""
    subprocess.call(
        [
            *YARN,
            "pa11y-ci-reporter-html",
            "--source",
            PA11Y_JSON,
            "--destination",
            PA11Y_BUILD,
        ],
        cwd=ROOT,
    )


def summary():
    """generate a summary and return the number of errors not ignored explicitly"""
    report = dict(
        HTML=REPORT_INDEX_URL, Roadmap=str(PA11Y_ROADMAP), JSON=str(PA11Y_JSON)
    )

    pa11y_json = json.loads(PA11Y_JSON.read_text())
    pa11y_roadmap = [
        line.split("#")[0].strip()
        for line in PA11Y_ROADMAP.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    error_codes = defaultdict(lambda: 0)

    for page, results in pa11y_json["results"].items():
        for result in results:
            if "code" in result:
                error_codes[result["code"]] += 1

    roadmap_counts = {}
    not_roadmap_counts = {}

    for code, count in sorted(error_codes.items()):
        code_on_roadmap = code in pa11y_roadmap
        if code_on_roadmap:
            roadmap_counts[code] = count
        else:
            not_roadmap_counts[code] = count

    report.update(
        {
            "total errors": pa11y_json["errors"],
            "on roadmap": roadmap_counts,
            "not on roadmap": not_roadmap_counts,
        }
    )

    nrc = sum(not_roadmap_counts.values())
    report["passed"] = nrc == 0
    report_str = safe_dump(report, default_flow_style=False)

    if os.environ.get("CI") and nrc:
        print("""::error ::{}""".format(report_str.replace("\n", "%0A")))
    else:
        print(report_str)

    return nrc


def main(no_serve=True):
    """start the server (if needed), then audit, report, and clean up"""
    clean()
    server = None
    try:
        if not no_serve:
            server = serve()
        audit()
        report()
    finally:
        server and server.terminate()

    error_count = summary()

    return error_count


if __name__ == "__main__":
    sys.exit(main(no_serve="--no-serve" in sys.argv))
