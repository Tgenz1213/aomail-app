/** @type {import('tailwindcss').Config} */
export const darkMode = "class";
export const content = ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"];
export const theme = {
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
        },
        animation: {
            slideIn: "slideIn 0.5s ease-out forwards",
            slideOut: "slideOut 0.5s ease-out forwards",
        },
    },
};
export const plugins = [require("@tailwindcss/forms")];
export const safelist = [
    {
        pattern: /(bg|text|ring|hover:bg|focus:bg|group-hover:text|group-active:text|group-focus:text)-(orange|blue|gray|red|green|yellow|stone)(-\d+)?$/,
        variants: ['hover', 'focus', 'active'],
    },
];

