/**
 * Webpack configuration for pydata-sphinx-theme.
 *
 * This script does a few primary things:
 *
 * - Generates a `webpack-macros.html` file that defines macros used
 *   to insert CSS / JS at various places in the main `layout.html` template.
 * - Compiles our translation files into .mo files so they can be bundled with the theme
 * - Compiles our SCSS and JS and places them in the _static/ folder
 * - Downloads and links FontAwesome and some JS libraries (Bootstrap, etc)
 */

const { resolve } = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const dedent = require("dedent");
const { Compilation } = require("webpack");

/*******************************************************************************
 * Compile our translation files
 */
const { exec } = require("child_process");
const localePath = resolve(__dirname, "src/pydata_sphinx_theme/locale");
exec(`pybabel compile -d ${localePath} -D sphinx`);

/*******************************************************************************
 * Paths for various assets (sources and destinations)
 */

const scriptPath = resolve(__dirname, "src/pydata_sphinx_theme/assets/scripts");
const staticPath = resolve(__dirname, "src/pydata_sphinx_theme/theme/pydata_sphinx_theme/static");
const vendorPath = resolve(staticPath, "vendor");

/*******************************************************************************
 * functions to load the assets in the html head
 * the css, and js (preload/scripts) are digested for cache busting
 * the fonts are loaded from vendors
 */

function stylesheet(css) { return `<link href="{{ pathto('_static/${css}', 1) }}?digest=${this.hash}" rel="stylesheet" />`; }
function preload(js) { return `<link rel="preload" as="script" href="{{ pathto('_static/${js}', 1) }}?digest=${this.hash}" />`; }
function script(js) { return `<script src="{{ pathto('_static/${js}', 1) }}?digest=${this.hash}"></script>`; }

/*******************************************************************************
 * the assets to load in the macro
 */
const theme_stylesheets = [
  "styles/theme.css", // basic sphinx css
  "styles/bootstrap.css", // all bootstrap 5 css with variable adjustments
  "styles/pydata-sphinx-theme.css", // all the css created for this specific theme
];
const theme_scripts = [
  "scripts/bootstrap.js",
  "scripts/pydata-sphinx-theme.js",
];

/*******************************************************************************
 * Cache-busting Jinja2 macros (`webpack-macros.html`) used in `layout.html`
 *
 * @param  {Compilation} the compilation instance to extract the hash
 * @return {String} the macro to inject in layout.html
 */
function macroTemplate({ compilation }) {

  return dedent(`\
    <!--
      AUTO-GENERATED from webpack.config.js, do **NOT** edit by hand.
      These are re-used in layout.html
    -->

    {% macro head_pre_assets() %}
      <!-- Loaded before other Sphinx assets -->
      ${theme_stylesheets.map(stylesheet.bind(compilation)).join("\n")}
    {% endmacro %}

    {% macro head_js_preload() %}
      <!-- Pre-loaded scripts that we'll load fully later -->
      ${theme_scripts.map(preload.bind(compilation)).join("\n")}
    {% endmacro %}

    {% macro body_post() %}
      <!-- Scripts loaded after <body> so the DOM is not blocked -->
      ${theme_scripts.map(script.bind(compilation)).join("\n")}
    {% endmacro %}
  `);
}

/*******************************************************************************
 * Bundle the modules to use them in the theme outputs
 */

const htmlWebpackPlugin = new HtmlWebpackPlugin({
  filename: resolve(staticPath, "webpack-macros.html"),
  inject: false,
  minify: false,
  css: true,
  templateContent: macroTemplate,
});

module.exports = {
  mode: "production",
  devtool: "source-map",
  entry: {
    "pydata-sphinx-theme": resolve(scriptPath, "pydata-sphinx-theme.js"),
    "bootstrap": resolve(scriptPath, "bootstrap.js"),
  },
  output: {
    filename: "scripts/[name].js",
    path: staticPath,
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
    },
    minimizer: [
      '...',
      new CssMinimizerPlugin(),
      new TerserPlugin({
        terserOptions: {
          parallel: true,
        }
      })]
  },
  module: {
    rules: [{
      test: /\.(sa|sc|c)ss$/,
      use: [
        // Extracts CSS for each JS file that includes CSS
        { loader: MiniCssExtractPlugin.loader },
        {
          // Interprets `@import` and `url()` like `import/require()` and will resolve them
          loader: 'css-loader',
          options: {
            sourceMap: true,
            url: true,
          }
        },
        { loader: 'resolve-url-loader' },
        {
          // Loads a SASS/SCSS file and compiles it to CSS
          loader: "sass-loader",
          options: {
            sourceMap: true,
            sassOptions: { outputStyle: "expanded" }
          }
        },
      ],
    },
    {
      // Font vendoring and management - will separate FA and export the font files
      test: /\.(woff|woff2|eot|ttf|otf)$/i,
      type: 'asset/resource',
      generator: {
        filename: 'vendor/fontawesome/webfonts/[name][ext]'
      }
    },],
  },
  plugins: [
    htmlWebpackPlugin,
    new MiniCssExtractPlugin({
      filename: "styles/[name].css",
      chunkFilename: "styles/[id].css",
    })],
  experiments: {
    topLevelAwait: true,
  },
};
