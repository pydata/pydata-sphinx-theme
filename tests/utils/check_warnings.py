"""Check the list of warnings produced by a doc build."""

import sys
from pathlib import Path

from colorama import Fore, init
from pydata_sphinx_theme.utils import escape_ansi

# init colors for all plateforms
init()


def check_warnings(file: Path) -> bool:
    """Check the list of warnings produced by a doc build.

    Raise errors if there are unexpected ones and/or if some are missing.

    Parameters:
        file: the path to the generated warning.txt file from
            the CI build

    Returns:
        0 if the warnings are all there
        1 if some warning are not registered or unexpected
    """
    # print some log
    print("\n=== Sphinx Warnings test ===\n")

    # find the file where all the known warnings are stored
    warning_file = Path(__file__).parent.parent / "warning_list.txt"
    extra_warning_file = Path(__file__).parent.parent / "intermittent_warning_list.txt"

    received_warnings = escape_ansi(file.read_text()).strip().split("\n")
    expected_warnings = warning_file.read_text().strip().split("\n")
    intermittent_warnings = extra_warning_file.read_text().strip().split("\n")
    # filter out empty warnings (happens on notebooks for some reason)
    received_warnings = list(filter(len, received_warnings))

    print(
        f'Checking build warnings in file: "{file}" and comparing to expected '
        f'warnings defined in "{warning_file}" and "{extra_warning_file}"\n\n'
    )

    for exp_w in expected_warnings[::-1] + intermittent_warnings[::-1]:
        found = False
        for rec_w in received_warnings:
            if exp_w in rec_w:
                received_warnings.remove(rec_w)
                if exp_w in expected_warnings:
                    expected_warnings.remove(exp_w)
                elif exp_w in intermittent_warnings:
                    intermittent_warnings.remove(exp_w)
                found = True
                break
        # alert only if an *always expected* warning wasn't raised (not intermittent)
        if not found and exp_w not in intermittent_warnings:
            print(f"{Fore.YELLOW}Warning was not raised: {Fore.RESET}{exp_w}\n")
    # warn about unexpected warnings
    for rec_w in received_warnings[::-1]:
        print(f"{Fore.YELLOW}Unexpected warning: {Fore.RESET}{rec_w}\n")
    return len(received_warnings) or len(expected_warnings)


if __name__ == "__main__":
    # cast the file to path and resolve to an absolute one
    file = Path.cwd() / "warnings.txt"

    # execute the test
    sys.exit(check_warnings(file))
