import love from 'eslint-config-love'
import sveltePlugin from 'eslint-plugin-svelte'
import svelteParser from 'svelte-eslint-parser'
import tsParser from '@typescript-eslint/parser'
import tsPlugin from '@typescript-eslint/eslint-plugin'
import commentsPlugin from '@eslint-community/eslint-plugin-eslint-comments'
import importPlugin from 'eslint-plugin-import'
import nPlugin from 'eslint-plugin-n'
import promisePlugin from 'eslint-plugin-promise'
import globals from 'globals'

export default [
  // 1. GLOBAL IGNORES
  {
    ignores: [
      '**/node_modules/**', '**/.svelte-kit/**', '**/build/**', '**/dist/**',
      '**/static/**', '**/documentation/**', '**/script/**', '*.config.js',
      '*.config.cjs', 'vite.config.ts', 'vitest.config.ts'
    ]
  },
  
  // 2. MAIN RULES (Strict for production, just like Sydseter wants!)
  {
    files: ['src/**/*.ts', 'src/**/*.js'],
    plugins: {
      '@typescript-eslint': tsPlugin,
      '@eslint-community/eslint-comments': commentsPlugin,
      'import': importPlugin,
      'n': nPlugin,
      'promise': promisePlugin
    },
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
      globals: { ...globals.browser, ...globals.node }
    },
    rules: {
      ...love.rules,
      // We are leaving the strict rules ON so we can fix them properly, 
      // but we will silence a few highly disruptive formatting ones.
      'no-plusplus': 'off',
      'require-unicode-regexp': 'off',
      'no-console': 'off',
      '@typescript-eslint/restrict-template-expressions': 'off'
    }
  },

  // 3. SVELTE FILES
  {
    files: ['**/*.svelte'],
    plugins: {
      svelte: sveltePlugin,
      '@typescript-eslint': tsPlugin
    },
    languageOptions: {
      parser: svelteParser,
      parserOptions: {
        parser: tsParser,
        project: null
      }
    },
    rules: {
      ...sveltePlugin.configs.recommended.rules,
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off'
    }
  },

  // 4. THE PRO MOVE: TEST FILES EXCEPTION
  // Magic numbers and unbound methods are expected and totally fine in test suites.
  {
    files: ['**/*.test.ts'],
    rules: {
      '@typescript-eslint/no-magic-numbers': 'off',
      '@typescript-eslint/unbound-method': 'off',
      '@typescript-eslint/no-empty-function': 'off'
    }
  }
]