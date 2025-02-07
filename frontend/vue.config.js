const { defineConfig } = require("@vue/cli-service");
const TerserPlugin = require("terser-webpack-plugin");
const WebpackObfuscator = require("webpack-obfuscator");

module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        ...(process.env.NODE_ENV === "development" && {
            server: {
                type: "https",
            },
            headers: {
                "Cross-Origin-Opener-Policy": "same-origin-allow-popups",
                "Cross-Origin-Embedder-Policy": "unsafe-none",
            },
            liveReload: true,
            watchFiles: {
                options: {
                    usePolling: true,
                },
            },
            allowedHosts: process.env.ALLOWED_HOSTS.split(",")
        }),
        ...(process.env.NODE_ENV === "production" && {
            productionSourceMap: true,
            headers: {
                // Handled by Nginx
            },
        }),
    },
    configureWebpack: (config) => {
        if (process.env.NODE_ENV === "production") {
            config.optimization = {
                minimize: true,
                minimizer: [
                    new TerserPlugin({
                        terserOptions: {
                            output: {
                                comments: false,
                            },
                            compress: {
                                drop_console: true,
                                drop_debugger: true,
                            },
                        },
                        extractComments: false,
                    }),
                ],
            };
            config.plugins.push(
                new WebpackObfuscator({
                    rotateStringArray: true,
                    stringArray: true,
                    stringArrayThreshold: 0.5,
                    deadCodeInjection: false,
                    deadCodeInjectionThreshold: 0.1,
                    debugProtection: false,
                    compact: true,
                    controlFlowFlattening: false,
                    controlFlowFlatteningThreshold: 0.75,
                })
            );
        }
    },
});
