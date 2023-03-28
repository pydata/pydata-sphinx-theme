from pathlib import Path
import sys

from colorama import Fore, init

# init colors for all plateforms
init()


def check_warnings(file):
    """
    Check the list of warnings produced by the GitHub CI tests
    raise errors if there are unexpected ones and/or if some are missing

    Args:
        file (pathlib.Path): the path to the generated warning.txt file from
            the CI build

    Return:
        0 if the warnings are all there
        1 if some warning are not registered or unexpected
    """

    # print some log
    print("\n=== Sphinx Warnings test ===\n")

    # find the file where all the known warnings are stored
    warning_file = Path(__file__).parent / "warning_list.txt"

    test_warnings = file.read_text().strip().split("\n")
    ref_warnings = warning_file.read_text().strip().split("\n")

    print(
        f'Checking build warnings in file: "{file}" and comparing to expected '
        f'warnings defined in "{warning_file}"\n\n'
    )

    # find all the missing warnings
    missing_warnings = []
    for wa in ref_warnings:
        index = [i for i, twa in enumerate(test_warnings) if wa in twa]
        if len(index) == 0:
            missing_warnings += [wa]
            print(f"{Fore.YELLOW}Warning was not raised: {Fore.RESET}{wa}\n")
        else:
            test_warnings.pop(index[0])

    # the remaining one are unexpected
    for twa in test_warnings:
        print(f"{Fore.YELLOW}Unexpected warning: {Fore.RESET}{twa}\n")

    return len(missing_warnings) != 0 or len(test_warnings) != 0


if __name__ == "__main__":
    # cast the file to path and resolve to an absolute one
    file = Path.cwd() / "warnings.txt"

    # execute the test
    sys.exit(check_warnings(file))
