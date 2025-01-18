/** @type {import('tailwindcss').Config} */
export default {
  content: [],
  content: ['./src/**/*.{html,svelte,js,ts}'],
  theme: {
    extend: {},
  },
  plugins: [],
  plugins: [require('daisyui')],
  daisyui: {
    themes: ["lofi"], // Specify the themes you want to include
  },
 }