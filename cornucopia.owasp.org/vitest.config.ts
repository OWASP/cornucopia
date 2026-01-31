import { defineConfig } from 'vitest/config';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
    resolve: {
        alias: {
            $lib: path.resolve(__dirname, './src/lib'),
            $domain: path.resolve(__dirname, './src/domain')
        }
    },
    test: {
        coverage: {
            enabled: true,
            provider: 'v8',
            reporter: ['text', 'json', 'lcov'],
            reportsDirectory: './coverage',
            thresholds: {
                autoUpdate: false,
                statements: 95,
                branches: 90,
                functions: 100,
                lines: 95
            },
            exclude: [
                'node_modules/',
                'dist/',
                '**/*.config.{js,ts}',
                '**/*.d.ts',
                'data/**',
                'cache/**',
                'script/**',
                'static/**',
                'src/scripts/**',
                'build/**',
                '.svelte-kit/**'
            ]
        },
        include: ['**/*.test.ts', '**/*.test.tsx'],
        exclude: [
            'node_modules/',
            'dist/',
            '**/*.config.{js,ts}',
            '**/*.d.ts',
            'data/**',
            'cache/**',
            'script/**',
            'static/**',
            'src/scripts/**',
            'build/**',
            '.svelte-kit/**'
        ]
    }
});