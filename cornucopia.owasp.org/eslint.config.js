import js from '@eslint/js';
import ts from 'typescript-eslint';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import tsParser from '@typescript-eslint/parser';
export default ts.config(
  js.configs.recommended,
  ...ts.configs.recommended,
  ...svelte.configs['flat/recommended'],
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node
      }
    }
  },
  {
    files: ['**/*.svelte'],
    languageOptions: {
      parserOptions: {
        parser: tsParser
      }
    }
  },
  {
    rules: {
      'svelte/no-navigation-without-resolve': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': ['error', {
        'varsIgnorePattern': '^_',
        'argsIgnorePattern': '^_',
        'caughtErrorsIgnorePattern': '^_'
      }]
    }
  },
  {
    ignores: ['build/', '.svelte-kit/', 'dist/', 'deploy/', 'coverage/']
  }
);