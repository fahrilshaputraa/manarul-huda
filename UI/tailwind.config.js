/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./node_modules/flowbite/**/*.js",
    "./src/**/*.{html,js}",
    "./*.html"
  ],
  theme: {
    colors: {
      'primary' : {
        50: '#F6FAEB',
        100: '#E9F4D3',
        200: '#D4EAAC',
        300: '#B8DC7C',
        400: '#9BCA51',
        500: '#7DAF33',
        600: '#608B25',
        700: '#4A6B20',
        800: '#3D551F',
        900: '#35491E',
        950: '#1A280B',
      }
    },
    extend: {
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

