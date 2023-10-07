const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    liveReload: true,
    watchFiles: {
      options: {
        usePolling: true
      }
    },
  }
})
