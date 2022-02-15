module.exports = {
  content: [
    './templates/*',
    './templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("daisyui"),
  ],
  important: true,
}
