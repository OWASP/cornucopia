import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    include: ['test/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'lcov'],
      reportsDirectory: './coverage',
      include: ['js/app.js'],
      exclude: ['vendor/**', 'build.js'],
      statements: 95,
      branches: 95,
      functions: 95,
      lines: 95
    }
  }
});
