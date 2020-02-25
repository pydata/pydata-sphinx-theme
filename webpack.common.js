const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: {
    theme: [
      './src/js/theme.js',
      './src/scss/theme.scss',
    ],
    // badge_only: './src/sass/badge_only.sass',
  },
  output: {
    filename: 'js/[name].js?[hash]',
    path: path.resolve(__dirname, 'pandas_sphinx_theme/static'),
  },
  module: {
    rules: [
      {
        // test: require.resolve('heme.js'),
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
          // {
          //   loader: 'postcss-loader',
          // },
          {
            loader: 'sass-loader',
          },
        ],
      },
    ],
  },
  plugins: [
  ],
};
