/**
 * Webpack configuration for pydata-sphinx-theme.
 *
 * This script does a few primary things:
 *
 * - Generates a `webpack-macros.html` file that defines macros used
 *   to insert CSS / JS at various places in the main `layout.html` template.
 * - Compiles our SCSS and JS and places them in the _static/ folder
 * - Downloads and links FontAwesome and some JS libraries (Bootstrap, jQuery, etc)
 */

const { resolve } = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const dedent = require("dedent");

//
// Paths for various assets (sources and destinations)
//
const staticPath = resolve(
  __dirname,
  "src/pydata_sphinx_theme/theme/pydata_sphinx_theme/static"
);
const vendor = resolve(staticPath, "vendor");
const vendorVersions = {
  fontAwesome: require("@fortawesome/fontawesome-free/package.json").version,
};
const vendorPaths = {
  fontAwesome: resolve(vendor, "fontawesome", vendorVersions.fontAwesome),
};

//
// Cache-busting Jinja2 macros (`webpack-macros.html`) used in `layout.html`
//
function macroTemplate({ compilation }) {
  const hash = compilation.hash;
  // We load these files into the theme via HTML templates
  const css_files = ["styles/theme.css", "styles/pydata-sphinx-theme.css"];
  const js_files = ["scripts/pydata-sphinx-theme.js"];

  // Load a CSS script with a digest for cache busting.
  function stylesheet(css) {
    return `<link href="{{ pathto('_static/${css}', 1) }}?digest=${hash}" rel="stylesheet">`;
  }

  // Pre-load a JS script (script will need to be loaded later on in the page)
  function preload(js) {
    return `<link rel="preload" as="script" href="{{ pathto('_static/${js}', 1) }}?digest=${hash}">`;
  }

  // Load a JS script with a digest for cache busting.
  function script(js) {
    return `<script src="{{ pathto('_static/${js}', 1) }}?digest=${hash}"></script>`;
  }

  return dedent(`\
    <!--
      AUTO-GENERATED from webpack.config.js, do **NOT** edit by hand.
      These are re-used in layout.html
    -->
    {# Load FontAwesome icons #}
    {% macro head_pre_icons() %}
      <link rel="stylesheet"
        href="{{ pathto('_static/vendor/fontawesome/${
          vendorVersions.fontAwesome
        }/css/all.min.css', 1) }}">
      <link rel="preload" as="font" type="font/woff2" crossorigin
        href="{{ pathto('_static/vendor/fontawesome/${
          vendorVersions.fontAwesome
        }/webfonts/fa-solid-900.woff2', 1) }}">
      <link rel="preload" as="font" type="font/woff2" crossorigin
        href="{{ pathto('_static/vendor/fontawesome/${
          vendorVersions.fontAwesome
        }/webfonts/fa-brands-400.woff2', 1) }}">
    {% endmacro %}

    {% macro head_pre_assets() %}
      <!-- Loaded before other Sphinx assets -->
      ${css_files.map(stylesheet).join("\n")}
    {% endmacro %}

    {% macro head_js_preload() %}
      <!-- Pre-loaded scripts that we'll load fully later -->
      ${js_files.map(preload).join("\n")}
    {% endmacro %}

    {% macro body_post() %}
      <!-- Scripts loaded after <body> so the DOM is not blocked -->
      ${js_files.map(script).join("\n")}
    {% endmacro %}
  `);
}

module.exports = {
  mode: "production",
  devtool: "source-map",
  entry: {
    "pydata-sphinx-theme": [
      "./src/pydata_sphinx_theme/assets/scripts/index.js",
    ],
  },
  output: {
    filename: "scripts/[name].js",
    path: staticPath,
  },
  optimization: {
    minimizer: [new TerserPlugin(), new OptimizeCssAssetsPlugin({})],
  },
  externals: {
    // Define jQuery as external, this way Sphinx related javascript
    // and custom javascript like popper.js can hook into jQuery.
    jquery: "jQuery",
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "styles/pydata-sphinx-theme.css",
            },
          },
          {
            loader: "extract-loader",
          },
          {
            // Use the css-loader with url()-inlining turned off.
            loader: "css-loader?-url",
          },
          {
            loader: "sass-loader",
          },
        ],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: resolve(staticPath, "webpack-macros.html"),
      inject: false,
      minify: false,
      css: true,
      templateContent: macroTemplate,
    }),
    new CopyPlugin([
      // fontawesome
      {
        context: "./node_modules/@fortawesome/fontawesome-free",
        from: "LICENSE.txt",
        to: resolve(vendorPaths.fontAwesome, "LICENSE.txt"),
      },
      {
        context: "./node_modules/@fortawesome/fontawesome-free/css",
        from: "all.min.css",
        to: resolve(vendorPaths.fontAwesome, "css"),
      },
      {
        context: "./node_modules/@fortawesome/fontawesome-free",
        from: "webfonts",
        to: resolve(vendorPaths.fontAwesome, "webfonts"),
      },
    ]),
  ],
};
