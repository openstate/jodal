/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  safelist: [
    'bg-gray-200',
    'hover:bg-gray-300',
    'text-blue-900',
    'px-1',
    'rounded',
    'cursor-pointer',
    'transition-colors',
    'duration-200',
    'inline',
    'whitespace-normal',
    'text-left'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

