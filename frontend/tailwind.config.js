/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0052FF', // Professional Blue
          50: '#eff4ff',
          100: '#dbeafe',
          500: '#0052FF',
          600: '#0043d6',
          900: '#1e3a8a',
        },
        secondary: {
          DEFAULT: '#10B981', // Professional Green
          50: '#ecfdf5',
          100: '#d1fae5',
          500: '#10B981',
          600: '#059669',
        },
        background: '#ffffff',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
