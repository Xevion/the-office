module.exports = {
  outputDir: '../dist/',
  assetsDir: './static',
  css: {
    loaderOptions: {
      sass: {
        prependData: '@import "@/scss/_variables.scss";'
      }
    }
  }
};
