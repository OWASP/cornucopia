import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import config from './svelte.config.js';

describe('svelte.config.js prerender error handling', () => {
	let consoleErrorSpy: ReturnType<typeof vi.spyOn>;

	beforeEach(() => {
		consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
	});

	afterEach(() => {
		consoleErrorSpy.mockRestore();
	});

	const { handleHttpError, handleMissingId } = config.kit.prerender;

	describe('handleHttpError', () => {
		it('throws Prerender SSR failure for HTTP 500 errors', () => {
			expect(() => {
				handleHttpError({
					status: 500,
					path: '/edition/webapp/VE2/3.0/en',
					referrer: null,
					referenceType: 'linked',
					message: 'Database/Loader crash'
				});
			}).toThrowError(
				'Prerender SSR failure (HTTP 500) on /edition/webapp/VE2/3.0/en: Database/Loader crash'
			);

			expect(consoleErrorSpy).toHaveBeenCalledOnce();
			const logOutput = consoleErrorSpy.mock.calls[0][0];
			expect(logOutput).toContain('HTTP 500 on /edition/webapp/VE2/3.0/en');
			expect(logOutput).toContain('Referrer: (direct entry)');
			expect(logOutput).toContain('Reference Type: linked');
			expect(logOutput).toContain('Message: Database/Loader crash');
		});

		it('throws Prerender route not found for HTTP 404 errors', () => {
			expect(() => {
				handleHttpError({
					status: 404,
					path: '/nonexistent-page',
					referrer: '/about',
					referenceType: 'linked',
					message: 'Not found'
				});
			}).toThrowError(
				'Prerender route not found (HTTP 404) on /nonexistent-page (linked from /about): Not found'
			);
		});

		it('throws Prerender HTTP error for other 4xx errors (e.g. 403, 400)', () => {
			expect(() => {
				handleHttpError({
					status: 403,
					path: '/admin',
					referrer: null,
					referenceType: 'linked',
					message: 'Forbidden'
				});
			}).toThrowError(
				'Prerender HTTP error (HTTP 403) on /admin: Forbidden'
			);
		});

		it('REGRESSION GUARD (#3639): fails the build on /edition and /mapping instead of silently returning', () => {
			// Historically, svelte.config.js silently swallowed errors on /mapping and /edition*
			expect(() => {
				handleHttpError({
					status: 500,
					path: '/mapping',
					referrer: null,
					referenceType: 'linked',
					message: 'SSR failed on mapping'
				});
			}).toThrow();

			expect(() => {
				handleHttpError({
					status: 500,
					path: '/edition/mobileapp/PC2/2.0/en',
					referrer: null,
					referenceType: 'linked',
					message: 'YAML load failure'
				});
			}).toThrow();

			expect(() => {
				handleHttpError({
					status: 404,
					path: '/edition/unknown/test',
					referrer: null,
					referenceType: 'linked',
					message: 'Not found'
				});
			}).toThrow();
		});
	});

	describe('handleMissingId', () => {
		it('ignores "card" id without throwing', () => {
			expect(() => {
				handleMissingId({
					_path: '/cards/AAA',
					id: 'card',
					_referrers: [],
					message: 'Missing element with id "card"'
				});
			}).not.toThrow();
		});

		it('throws on any other missing element id', () => {
			expect(() => {
				handleMissingId({
					_path: '/cards/AAA',
					id: 'unexpected-id',
					_referrers: [],
					message: 'Missing element with id "unexpected-id"'
				});
			}).toThrowError('Missing element with id "unexpected-id"');
		});
	});
});
