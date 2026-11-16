import { designerPythonLoader } from '@disguise-one/designer-pythonapi/vite-loader'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    designerPythonLoader(),
    tailwindcss(),
    svelte({
      compilerOptions: {
        // Force runes mode for the project, except for libraries.
        // Can be removed in svelte 6.
        runes: ({ filename }) =>
          filename.split(/[/\\]/).includes('node_modules') ? undefined : true,
      },
      onwarn(warning, defaultHandler) {
        if (warning.code === 'css_unused_selector') return
        defaultHandler(warning)
      },
    }),
  ],
  resolve: { tsconfigPaths: true },
  build: {
    minify: false,
    // oxfmt-ignore
    rolldownOptions:{ output:{ codeSplitting:{ groups:[
      { test: /node_modules/, name: 'libs' },
    ]}}},
  },
})
