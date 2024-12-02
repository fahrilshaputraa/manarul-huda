/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./node_modules/flowbite/**/*.js",
    "./src/**/*.{html,js}",
    "./../templates/**/*.html"
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
      },
      'gray': {
        50: '#f6f6f6',
        100: '#e7e7e7',
        200: '#d1d1d1',
        300: '#b0b0b0',
        400: '#888888',
        500: '#6d6d6d',
        600: '#5d5d5d',
        700: '#4f4f4f',
        800: '#454545',
        900: '#333333',
        950: '#262626',
      }
    },
    extend: {
    },
  },
  plugins: [
    require('flowbite/plugin'),
    require('@tailwindcss/typography'),
  ],
}

