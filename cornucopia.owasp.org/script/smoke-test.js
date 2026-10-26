import { getSvelteEntries } from './app-config.js';

const baseUrl = 'http://localhost:3000';

async function runSmokeTest() {
    console.log('Starting smoke tests...');

    const entries = getSvelteEntries([]);

    console.log(`Found ${entries.length} pages to test.`);

    let failed = false;
    for (const entry of entries) {
        const url = `${baseUrl}${entry}`;
        try {
            const response = await fetch(url);
            if (response.ok) {
                console.log(`[PASS] ${url} (${response.status})`);
            } else {
                console.error(`[FAIL] ${url} (${response.status})`);
                failed = true;
            }
        } catch (error) {
            console.error(`[ERROR] ${url}: ${error.message}`);
            failed = true;
        }
    }

    if (failed) {
        console.error('Smoke tests failed!');
        process.exit(1);
    } else {
        console.log('All smoke tests passed!');
    }
}

runSmokeTest();
