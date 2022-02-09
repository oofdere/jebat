module.exports = {
  content: [
    './templates/*',
    './templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),

  ],
  important: true,
}
