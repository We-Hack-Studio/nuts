// Configurations in this file will be merged into the final webpack config using webpack-merge.
// Ref: https://cli.vuejs.org/guide/webpack.html

'use strict'

const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    publicPath: '/static/',
    configureWebpack: {
        plugins: [
            new BundleTracker({filename: './webpack-stats.json'}),
        ]
    }
}