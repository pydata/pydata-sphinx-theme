const path = require('path');
const merge = require('webpack-merge');
const exec = require('child_process').exec;
const WatchPlugin = require('webpack-watch-files-plugin').default;
const ShellPlugin = require('webpack-shell-plugin');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  watch: true,
  devServer: {
    contentBase: path.join(__dirname, 'docs/_build/html'),
    watchContentBase: true,
    compress: false,
    port: 1919,
    hot: false,
    liveReload: true,
    publicPath: '/_static/',
    writeToDisk: true,
  },
  plugins: [
    new WatchPlugin({
      files: [
        './docs/**/*.rst',
        './docs/**/*.py',
        './pydata_sphinx_theme/**/*.html',
        './pydata_sphinx_theme/**/*.css',
        // watching the generated macros causes vicious cycles
        '!./pydata_sphinx_theme/static/*.html',
      ],
    }),
    new ShellPlugin({
      onBuildEnd: ['make -C docs clean html'],
      // dev=false here to force every build to trigger make, the default is
      // first build only.
      dev: false,
    }),
  ],
});
