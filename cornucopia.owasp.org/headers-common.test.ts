import { afterEach, describe, expect, it, vi } from 'vitest';
import fs from 'node:fs';
import { writeHeaders } from './script/headers-common.js';

afterEach(() => {
	vi.restoreAllMocks();
});

describe('Cloudflare fallback headers', () => {
	it.each(['stage', 'production'] as const)(
		'serves the fallback as HTML without overriding static asset MIME types in %s',
		(environment) => {
			const write = vi.spyOn(fs, 'writeFileSync').mockImplementation(() => {});

			writeHeaders({ buildDir: 'build', environment });

			expect(write).toHaveBeenCalledOnce();
			const output = String(write.mock.calls[0][1]);
			const rules = output.trim().split(/\n(?=\/)/);
			expect(rules.filter(rule => rule.startsWith('/error\n'))).toEqual([
				'/error\n  ! Content-Type\n  Content-Type: text/html; charset=utf-8'
			]);
			expect(rules.find(rule => rule.startsWith('/*\n'))).not.toContain('Content-Type:');
		}
	);
});
