"""Script to profile the build of the test site with py-spy.

This can be called with `python tools/profile.py` and will profile the build of the test site.
You can additionally configure the number of extra pages to add to the build with the `-n` flag and the output file with the `-o` flag.

$ python tools/profile.py -n 100 -o profile.svg

If running within tox (recommended) this can be run with:

$ tox -e profile-docs -- -n 100 -o profile.svg

"""

import argparse
import shutil as sh
import subprocess
import tempfile
from pathlib import Path
from textwrap import dedent


def profile_docs(output: str = "profile.svg", n_extra_pages: int = 50) -> None:
    """Add a bunch of extra pages to the test site and profile the build with py-spy.

    Args:
        output (str): The output filename for generated chart, defaults to output.svg.
        n_extra_pages (int): The number of extra pages to add to the build, defaults to 50.
    """
    # base path of the test site
    base_site_path = Path("tests/sites/base")

    with tempfile.TemporaryDirectory() as tmpdir:

        # copy over the base test site to the temporary folder
        target_path = Path(tmpdir) / base_site_path
        sh.copytree(base_site_path, target_path)
        print(f"Copied {base_site_path} to {target_path}")

        # Add a bunch of extra files to increase the build length
        index_file = target_path / "index.rst"
        dummy_text = index_file.read_text()
        dummy_text += dedent(
            """
        .. toctree::
            :glob:

            many/*
        """
        )
        index_file.write_text(dummy_text)
        many_files_path = target_path / "many"
        try:
            many_files_path.mkdir(parents=False)
        except FileNotFoundError:
            print(f"Could not create directory {many_files_path}")

        # create a bunch of empty pages to slow the build
        for page in range(n_extra_pages):
            (many_files_path / f"{page}.rst").write_text("Test\n====\n\nbody\n")

        # Output directory
        output_site_path = target_path / "_build"

        # Profile the build
        print(f"Profiling build with {n_extra_pages} pages with py-spy...")

        subprocess.run(
            [
                "py-spy",
                "record",
                "-o",
                output,
                "--",
                "sphinx-build",
                target_path,
                f" {output_site_path}/_build",
            ],
            capture_output=True,
        )

    print("py-spy profiler output at this file:", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-o", "--output", type=str, help="Output filename, the default is profile.svg"
    )
    parser.add_argument(
        "-n", "--n_pages", type=int, help="Number of extra pages to add to the build"
    )

    # Parse the arguments
    args = parser.parse_args()
    output_file = args.output if args.output else "profile.svg"
    n_pages = args.n_pages if args.n_pages else 50

    profile_docs(output=output_file, n_extra_pages=n_pages)
