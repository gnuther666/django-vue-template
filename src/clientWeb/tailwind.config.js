/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html","./src/views/*.{vue,js,ts}", 
    "./src/views/**/*.{vue,js,ts}",
    "./src/components/**/*.{vue,js,ts}", "./src/components/*.{vue,js,ts}"],
  theme: {
    extend: {},
  },
  plugins: [],
  mode: 'jit', // Enable Just-In-Time mode
}

