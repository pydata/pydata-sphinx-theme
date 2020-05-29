const path = require('path');

module.exports = {
  entry: {
    index: ['./src/js/index.js'],
  },
  output: {
    filename: 'js/[name].js?[hash]',
    path: path.resolve(__dirname, 'pydata_sphinx_theme/static'),
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
};
