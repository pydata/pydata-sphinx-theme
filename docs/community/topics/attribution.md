# Ignore formatting commits with `git blame`

When making commits that are strictly formatting/style changes (e.g., after running a new version of black or running pyupgrade after dropping an old Python version), add the commit hash to `.git-blame-ignore-revs`, so `git blame` can ignore the change.

For more details, see:

- https://git-scm.com/docs/git-config#Documentation/git-config.txt-blameignoreRevsFile
- https://github.com/pydata/pydata-sphinx-theme/pull/713
