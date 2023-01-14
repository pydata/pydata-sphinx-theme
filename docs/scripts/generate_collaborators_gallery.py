"""Uses the GitHub API to list a gallery of all people with direct access
to the repository.
"""

from yaml import dump
from subprocess import run
import shlex
import json
from pathlib import Path

COLLABORATORS_API = "https://api.github.com/repos/pydata/pydata-sphinx-theme/collaborators?affiliation=direct"  # noqa

print("Grabbing latest collaborators with GitHub API via GitHub's CLI...")
out = run(shlex.split(f"gh api {COLLABORATORS_API}"), capture_output=True)
collaborators = json.loads(out.stdout.decode())
path_docs_source = Path(__file__).parent.parent
path_collaborators = path_docs_source / "_static/contributors.yaml"
contributor_yaml = []
for collaborator in collaborators:
    # contributor_yaml =
    contributor_yaml.append(
        {
            "header": f"@{collaborator['login']}",
            "image": f"https://avatars.githubusercontent.com/u/{collaborator['id']}",
            "website": collaborator["html_url"],
        }
    )

print("Writing collaborator YAML to disk...")
path_collaborators.touch()
with path_collaborators.open("w+") as ff:
    dump(contributor_yaml, ff)
print("Finished!")
