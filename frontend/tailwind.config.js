/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        serif: ['"Instrument Serif"', 'Georgia', 'serif'],
        sans:  ['"Geist"', 'system-ui', 'sans-serif'],
      },
      colors: {
        bg:       '#0D0D0D',
        surface:  '#161616',
        surface2: '#1E1E1E',
        accent:   '#E8C547',
        muted:    '#6B6661',
        muted2:   '#4A4643',
        ink:      '#F0EDE8',
        green:    '#4ADE80',
      },
      animation: {
        breathe: 'breathe 2.5s ease-in-out infinite',
        fadeUp:  'fadeUp 0.6s ease both',
        spin:    'spin 0.7s linear infinite',
      },
      keyframes: {
        breathe: { '0%,100%': { opacity: 1 }, '50%': { opacity: 0.4 } },
        fadeUp:  { from: { opacity: 0, transform: 'translateY(18px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [],
}
