const { resolve } = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

const staticPath = resolve(__dirname, 'pydata_sphinx_theme/static');
const vendor = resolve(staticPath, 'vendor');

module.exports = {
  entry: {
    index: ['./src/js/index.js', './src/scss/index.scss'],
  },
  output: {
    filename: 'js/[name].js?[hash]',
    path: staticPath,
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: 'imports-loader?this=>window',
      },
      {
        test: /\.scss$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: 'css/[name].css',
            },
          },
          {
            loader: 'extract-loader',
          },
          {
            loader: 'css-loader?-url',
          },
          {
            loader: 'sass-loader',
          },
          // {
          //   loader: 'postcss-loader',
          // },
        ],
      },
    ],
  },
  plugins: [
    new CleanWebpackPlugin(),
    new CopyPlugin([
      // bootstrap
      {
        // includes popper.js
        context: './node_modules/bootstrap/dist/js/',
        from: 'bootstrap.bundle.min.*',
        to: resolve(vendor, 'bootstrap')
      },
      {
        context: './node_modules/bootstrap/',
        from: 'LICENSE',
        to: resolve(vendor, 'bootstrap')
      },
      // fonts
      {
        context: './node_modules/@fortawesome/fontawesome-free/css',
        from: 'all.min.css',
        to: resolve(vendor, 'fontawesome', 'css')
      },
      {
        context: './node_modules/@fortawesome/fontawesome-free',
        from: 'webfonts',
        to: resolve(vendor, 'fontawesome', 'webfonts')
      },
      {
        context: './node_modules/@fortawesome/fontawesome-free',
        from: 'LICENSE.txt',
        to: resolve(vendor, 'fontawesome')
      },
      {
        context: './node_modules/@openfonts/open-sans_all',
        from: 'files/*-400*',
        to: resolve(vendor, 'open-sans_all')
      },
      {
        context: './node_modules/@openfonts/open-sans_all',
        from: 'index.css',
        to: resolve(vendor, 'open-sans_all')
      },
      {
        context: './node_modules/@openfonts/open-sans_all',
        from: 'LICENSE.md',
        to: resolve(vendor, 'open-sans_all')
      },
      {
        context: './node_modules/@openfonts/lato_latin-ext',
        from: 'files/*-400*',
        to: resolve(vendor, 'lato_latin-ext')
      },
      {
        context: './node_modules/@openfonts/lato_latin-ext',
        from: 'index.css',
        to: resolve(vendor, 'lato_latin-ext')
      },
      {
        context: './node_modules/@openfonts/lato_latin-ext',
        from: 'LICENSE.md',
        to: resolve(vendor, 'lato_latin-ext')
      },
      // mathjax
      {
        context: './node_modules/mathjax',
        from: '*.js',
        to: resolve(vendor, 'mathjax')
      },
      {
        context: './node_modules/mathjax',
        from: 'jax/output/HTML-CSS',
        to: resolve(vendor, 'mathjax/jax/output/HTML-CSS')
      },
      {
        context: './node_modules/mathjax',
        from: 'fonts/HTML-CSS/TeX',
        to: resolve(vendor, 'mathjax/fonts/HTML-CSS/TeX')
      },
      {
        context: './node_modules/mathjax',
        from: 'config/TeX-AMS-MML_HTMLorMML.js',
        to: resolve(vendor, 'mathjax/config')
      },
      {
        context: './node_modules/mathjax',
        from: 'LICENSE',
        to: resolve(vendor, 'mathjax')
      },
    ])
  ],
};
