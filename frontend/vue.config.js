// Configurations in this file will be merged into the final webpack config using webpack-merge.
// Ref: https://cli.vuejs.org/guide/webpack.html

'use strict'

module.exports = {
    css: {
      loaderOptions: {
        sass: {
            prependData: `@import "~bootstrap/scss/bootstrap";@import "@/assets/_variable.scss";`
        }
      }
    }
  };