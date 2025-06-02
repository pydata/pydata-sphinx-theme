The purpose of files in this directory is to output CSS variables, not to define
Sass/SCSS variables for import elsewhere.

> [!TIP]
> ```
> // Put SCSS files in this folder that look like this
> :root {
>   --pst-example-css-variable: 1em;
> }
> ```

> [!CAUTION]
> ```
> // Do not put SCSS that defines SCSS variables
> $example-scss-variables: 1em;
> ```
