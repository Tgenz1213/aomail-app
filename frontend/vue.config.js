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
            allowedHosts: ["aomail.ai", "jean.aomail.ai", "augustin.aomail.ai", "theo.aomail.ai", "localhost"],
        }),
        ...(process.env.NODE_ENV === "production" && {
            productionSourceMap: true,
            headers: {
                "Content-Security-Policy":
                    "default-src 'self'; frame-ancestors 'self'; img-src https: data:; script-src 'self' https://cdn.quilljs.com/;",
                "X-Frame-Options": "DENY",
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
                "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            },
            allowedHosts: ["aomail.ai", "app.aomail.ai"],
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
