# Using `pre-commit`

Here are a few tips for using `pre-commit`:

## Skip the pre-commit checks

Run the following command:

```console
$ git commit --no-verify
```

## Run pre-commit on all files

By default, `pre-commit` will run its checks on files that have been modified in a commit.
To instead run it on all files, use this command:

```console
$ pre-commit run --all-files

# Alternatively
$ pre-commit run -a
```
