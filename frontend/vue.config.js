const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
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
    },
});
