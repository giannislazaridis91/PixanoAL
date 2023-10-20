/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{svelte,js,ts}",
    "../../../ui/components/core/src/**/*.{svelte,js,ts}",
    "../../../ui/components/table/src/**/*.{svelte,js,ts}",
    "../../../ui/components/canvas2d/src/**/*.{svelte,js,ts}",
  ],
  darkMode: "media", // or 'class'
  theme: {
    extend: {
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
      },
      colors: {
        main: "#771E5F",
      },
    },
  },
  plugins: [],
};
