SCSS files in this directory should NOT output any actual CSS. They are intended
purely for import by other SCSS files that output CSS.


> [!TIP]
> ```
> // Put SCSS that defines SCSS variables, functions, and mixins in this folder.
> // SCSS variables are NOT THE SAME as CSS variables. 
> $example-scss-variable: 0.0875rem
> @function example-function($n) {
>   @return 2 * $n;
> }
> @mixin example-mixin {
>   line-height: 2;
> }
> ```


> [!CAUTION]
> ```
> // Don't put any SCSS code that outputs actual CSS in this folder.
> // Do not define CSS variables in this folder.
> :root {
>   --pst-example-css-variable: 1em;
> }
> ```
