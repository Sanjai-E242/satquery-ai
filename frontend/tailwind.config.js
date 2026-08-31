/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        space: {
          950: '#060911',
          900: '#0B0F19',
          850: '#111726',
          800: '#172033',
          700: '#23304A',
          600: '#34466B',
        },
        cyanAccent: {
          400: '#38BDF8',
          500: '#00E5FF',
          600: '#00B4D8',
        },
        satellite: {
          green: '#10B981',
          blue: '#3B82F6',
          amber: '#F59E0B',
          rose: '#F43F5E',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      backgroundImage: {
        'grid-pattern': "radial-gradient(rgba(56, 189, 248, 0.08) 1px, transparent 0)",
        'spatial-glow': "radial-gradient(circle at 50% 0%, rgba(0, 229, 255, 0.12) 0%, transparent 60%)"
      }
    },
  },
  plugins: [],
};
