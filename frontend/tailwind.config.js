/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      boxShadow: {
        panel: '0 8px 32px rgba(0, 0, 0, 0.35)',
      },
    },
  },
  plugins: [],
}
