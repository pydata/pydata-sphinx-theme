# This code taken from:
# https://github.com/mozilla-services/axe-selenium-python/blob/3cfbdd67c9b40ab03f37b3ba2521f77c2071827b/axe_selenium_python/axe.py
# Typical usage:
# assert(len(results["violations"])) = 0, pretty_axe_results(results)
def pretty_axe_results(results: dict) -> str:
    """
    Return readable report of accessibility violations found.
    :param results: The object promised by `axe.run()`.
    :type results: dict
    :return report: Readable report of violations.
    :rtype: string
    """
    violations = results["violations"]
    string = ""
    string += "Found " + str(len(violations)) + " accessibility violations:"
    for violation in violations:
        string += (
            "\n\n\nRule Violated:\n"
            + violation["id"]
            + " - "
            + violation["description"]
            + "\n\tURL: "
            + violation["helpUrl"]
            + "\n\tImpact Level: "
            + violation["impact"]
            + "\n\tTags:"
        )
        for tag in violation["tags"]:
            string += " " + tag
        string += "\n\tElements Affected:"
        i = 1
        for node in violation["nodes"]:
            for target in node["target"]:
                string += "\n\t" + str(i) + ") Target: " + target
                i += 1
            for item in node["all"]:
                string += "\n\t\t" + item["message"]
            for item in node["any"]:
                string += "\n\t\t" + item["message"]
            for item in node["none"]:
                string += "\n\t\t" + item["message"]
        string += "\n\n\n"
    return string
