# Ignore formatting commits with `git blame`

Please follow these steps to avoid obscuring file history when making commits that are
strictly formatting/style changes (e.g., after running a new version of black or running
pyupgrade after dropping an old Python version).

1. Create a new branch.
2. Make any linting and formatting rules needed; either in the `pre-commit.config.yaml`
   or in the `pyproject.toml` file.
3. Commit your changes with the `--no-verify` flag to skip the pre-commit hooks.
4. Run the pre-commit hooks manually with `tox run -e lint` or `pre-commit run --all-files`.
5. Commit the linting and formatting changes.
6. Open a PR with these changes.

   ```{important}
   This PR **must** be rebase-merged -- instead of the default squash-merge we
   currently follow -- so a repository admin needs to enable this setting in the
   repository temporarily.

   ```

7. Open a new PR adding the commit hashes of the formatting commits to the `.git-blame-ignore-revs` file.

For more details, see:

- <https://git-scm.com/docs/git-config#Documentation/git-config.txt-blameignoreRevsFile>
- <https://github.com/pydata/pydata-sphinx-theme/pull/713>
