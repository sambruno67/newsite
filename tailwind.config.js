/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./innovgeomatic/templates/**/*.html",
    "./home/templates/**/*.html",
    "./services/templates/**/*.html",
    "./formations/templates/**/*.html",
    "./projets/templates/**/*.html",
    "./contact/templates/**/*.html",
    "./blog/templates/**/*.html",
    "./apropos/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: '#1A3A8F', dark: '#0F2460', light: '#2449B0' },
        sky:  { DEFAULT: '#29ABE2', light: '#E8F6FC', dark: '#1D9ED4' },
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        body:    ['DM Sans', 'sans-serif'],
      },
    }
  },
  plugins: [],
}