import { defineConfig } from 'oxfmt'

export default defineConfig({
  printWidth: 100,
  tabWidth: 2,
  semi: false,
  singleQuote: true,
  sortTailwindcss: true,
  sortPackageJson: false,
  svelte: { indentScriptAndStyle: false },
  overrides: [
    {
      files: ['*.css', '*.html'],
      options: { singleQuote: false },
    },
  ],
})
