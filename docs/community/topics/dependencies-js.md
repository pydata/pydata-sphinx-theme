# Update JavaScript dependencies and their versions

There are two kinds of dependency definitions in this theme:

- `package.json` contains the **base dependencies** for this theme. They are broken down into a few categories like `dependencies` and `devDependencies`. It is edited by the maintainers.
- `package-lock.json` contains the complete **frozen dependency chain** for this theme, including all sub-dependencies of our base dependencies. It is automatically generated.

To update or add a JS dependency, follow these steps:

1. **Edit `package.json`** by adding or modifying a dependency.
2. **Re-generate `package-lock.json`** in order to create a new set of frozen dependencies for the theme. To do this, run the following command from [the Sphinx Theme Builder](https://github.com/pradyunsg/sphinx-theme-builder).

   ```
   stb npm install --include=dev
   ```

3. **Commit both files** to the repository. When new people pull in the latest commits, their `npm` environment will automatically update according to the new lockfile.
