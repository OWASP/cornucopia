import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const baseUrl = 'http://localhost:3000';
const configPath = path.resolve(__dirname, '../svelte.config.js');

async function runSmokeTest() {
    console.log('Starting smoke tests...');
    
    // Read svelte.config.js to get entries
    const configContent = fs.readFileSync(configPath, 'utf-8');
    const entriesMatch = configContent.match(/entries: \[([\s\S]*?)\]/);
    
    if (!entriesMatch) {
        console.error('Could not find entries in svelte.config.js');
        process.exit(1);
    }
    
    const entriesRaw = entriesMatch[1];
    const entries = entriesRaw
        .split(',')
        .map(e => e.trim().replace(/['"\r\n]/g, ''))
        .filter(e => e.length > 0);

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
