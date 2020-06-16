const { resolve } = require('path');
const webpack = require('webpack');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

const staticPath = resolve(__dirname, 'pydata_sphinx_theme/static');
const vendor = resolve(staticPath, 'vendor');

module.exports = {
  entry: {
    index: ['./src/js/index.js'],
  },
  output: {
    filename: 'js/[name].js?[hash]',
    path: staticPath,
  },
  externals: {
    // Define jQuery as external, this way Sphinx related javascript
    // and custom javascript like popper.js can hook into jQuery.
    jquery: 'jQuery',
  },
  module: {
    rules: [
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
    ]),
    new webpack.ProvidePlugin({
      '$': "jquery",
      'jQuery': "jquery",
      'Popper': 'popper.js'
    }),
  ],
};
