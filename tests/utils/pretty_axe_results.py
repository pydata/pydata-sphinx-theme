"""Readable report of accessibility violations."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This code taken from:
# https://github.com/mozilla-services/axe-selenium-python/blob/3cfbdd67c9b40ab03f37b3ba2521f77c2071827b/axe_selenium_python/axe.py
# Typical usage:
# assert(len(results["violations"])) == 0, pretty_axe_results(results)


def pretty_axe_results(results: dict, selector: str) -> str:
    """Create readable string that can be printed to console from the Axe-core results object.

    :param results: The object promised by `axe.run()`.
    :type results: dict
    :return report: Readable report of violations.
    :rtype: string.

    """
    violations = results["violations"]
    string = ""
    string += f"Found {len(violations)} accessibility violations:"
    for violation in violations:
        string += (
            f"\n\n\nRule Violated:\n {violation['id']} - {violation['description']} \n\t"
            f"URL: {violation['helpUrl']} \n\t"
            f"Impact Level: {violation['impact']} \n\tTags:"
        )
        for tag in violation["tags"]:
            string += f" {tag}"
        string += f"\n\tTested selector: {selector}"
        string += "\n\tElements Affected:"
        i = 1
        for node in violation["nodes"]:
            for target in node["target"]:
                string += f"\n\t {i} Target: {target}"
                i += 1
            for item in node["all"]:
                string += f"\n\t\t {item['message']}"
            for item in node["any"]:
                string += f"\n\t\t {item['message']}"
            for item in node["none"]:
                string += f"\n\t\t {item['message']}"
        string += "\n\n\n"
    return string
