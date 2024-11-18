import forms from "@tailwindcss/forms";

/** @type {import('tailwindcss').Config} */
export default {
    darkMode: "class",
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {
            keyframes: {
                slideIn: {
                    "0%": { transform: "translateX(100%)" },
                    "100%": { transform: "translateX(0)" },
                },
                slideOut: {
                    "0%": { transform: "translateX(0)" },
                    "100%": { transform: "translateX(100%)" },
                },
                marquee: {
                    "0%": { transform: "translateX(100%)" },
                    "100%": { transform: "translateX(-100%)" },
                },
            },
            animation: {
                slideIn: "slideIn 0.5s ease-out forwards",
                slideOut: "slideOut 0.5s ease-out forwards",
                marquee: "marquee 30s linear infinite",
            },
        },
    },
    plugins: [forms],
    safelist: [
        {
            pattern:
                /(bg|text|stroke|ring|hover:bg|focus:bg|group-hover:text|group-active:text|group-focus:text)-(orange|blue|gray|red|green|yellow|stone)(-\d+)?$/,
            variants: ["hover", "focus", "active"],
        },
    ],
};
