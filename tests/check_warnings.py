from pathlib import Path
import sys

from colorama import Fore, init

# init colors for all plateforms
init()


def check_warnings(file):
    """
    Check the list of warnings produced by the GitHub CI tests
    raise errors if there are unexpected ones and/or if some are missing
    """

    # print some log
    print("\n=== Sphinx Warnings test ===\n\n")

    # find the file where all the known warnings are stored
    warning_file = Path(__file__).parent / "warning_list.txt"

    test_warnings = file.read_text().strip().split("\n")
    ref_warnings = warning_file.read_text().strip().split("\n")

    # find all the missing warnings
    missing_warnings = []
    for w in ref_warnings:
        try:
            test_warnings.pop(test_warnings.index(w))
        except ValueError:
            missing_warnings += [w]
            print(f"{Fore.YELLOW}Warning was not raised: {Fore.RESET}{w}\n")

    # the remaining one are unexpected
    for w in test_warnings:
        print(f"{Fore.YELLOW}Unexpected warning: {Fore.RESET}{w}")

    return len(missing_warnings) != 0 or len(test_warnings) != 0


if __name__ == "__main__":

    # cast the file to path and resolve to an absolute one
    file = Path.cwd() / "warnings.txt"

    # execute the test
    sys.exit(check_warnings(file))
