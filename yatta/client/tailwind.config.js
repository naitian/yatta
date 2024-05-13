import daisyui from 'daisyui';
import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  plugins: [
    typography,
    daisyui
  ],
  theme: {
    extend: {},
  },
  content: ["./index.html", './src/**/*.{svelte,js,ts}'], // for unused CSS
  variants: {
    extend: {},
  },
  darkMode: false, // or 'media' or 'class'
  daisyui: {
    themes: ["light"],
  }
}
