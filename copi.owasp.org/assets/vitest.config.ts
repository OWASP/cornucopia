import { defineConfig } from 'vitest/config';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const testDir = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      phoenix_html: path.resolve(testDir, 'test/stubs/phoenix_html.ts'),
      phoenix: path.resolve(testDir, 'test/stubs/phoenix.ts'),
      phoenix_live_view: path.resolve(testDir, 'test/stubs/phoenix_live_view.ts')
    }
  },
  test: {
    environment: 'jsdom',
    include: ['test/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'lcov'],
      reportsDirectory: './coverage',
      include: ['js/app.js'],
      exclude: ['vendor/**', 'build.js'],
      thresholds: {
        statements: 95,
        branches: 95,
        functions: 95,
        lines: 95
      }
    }
  }
});
