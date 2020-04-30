const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

const staticPath = path.resolve(__dirname, 'pydata_sphinx_theme/static');

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
      {
        // includes popper.js
        context: './node_modules/bootstrap/dist/js/',
        from: 'bootstrap.bundle.min.*',
        to: path.resolve(staticPath, 'vendor', 'bootstrap')
      },
      {
        context: './node_modules/@fortawesome/fontawesome-free/css',
        from: 'all.min.css',
        to: path.resolve(staticPath, 'vendor', 'fontawesome', 'css')
      },
      {
        context: './node_modules/@fortawesome/fontawesome-free',
        from: 'webfonts',
        to: path.resolve(staticPath, 'vendor', 'fontawesome', 'webfonts')
      },
    ])
  ],
};
