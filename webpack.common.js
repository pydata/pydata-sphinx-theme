const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  entry: {
    index: ['./src/js/index.js', './src/scss/index.scss'],
  },
  output: {
    filename: 'js/[name].js?[hash]',
    path: path.resolve(__dirname, 'pydata_sphinx_theme/static'),
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
  plugins: [new CleanWebpackPlugin()],
};
