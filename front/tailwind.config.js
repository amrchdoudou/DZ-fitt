/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'primary-blue': '#0940BE',
                'primary-green': '#B3F90F',
            },
            fontFamily: {
                hero: ['Monigue DEMO', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
