import { skeleton } from '@skeletonlabs/tw-plugin';
import forms from '@tailwindcss/forms';

const config = {
  darkMode: 'class',
  content: [
    './src/**/*.{html,js,svelte,ts}',
    // Specify the path to @skeletonlabs/skeleton manually
    './node_modules/@skeletonlabs/skeleton/**/*.html', // Adjust the path as necessary
    './node_modules/@skeletonlabs/skeleton/**/*.js',
    './node_modules/@skeletonlabs/skeleton/**/*.svelte',
    './node_modules/@skeletonlabs/skeleton/**/*.ts',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          '600': '#3B82F6',
        },
        error: {
          '700': '#EF4444',
        }
      }
    },
  },
  plugins: [
    skeleton({
      themes: {
        preset: [
          {name: "skeleton",enhancements:true},{name: "modern",enhancements:true},{name: "wintry",enhancements:true},{name: "crimson",enhancements:true}
        ],
      },
    }),
    forms,
  ],
};

export default config;
