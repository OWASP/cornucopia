import fs from 'fs';
import path from 'path';

const __dirname = path.resolve();
let buildDir = '';
if (fs.existsSync(path.join(__dirname, '.vercel/output'))) {
  buildDir = path.join(__dirname, '.vercel/output');
} else if (fs.existsSync(path.join(__dirname, 'build'))) {
  buildDir = path.join(__dirname, 'build');
} else if (fs.existsSync(path.join(__dirname, 'output'))) {
  buildDir = path.join(__dirname, 'output');
} else {
  process.exit(0);
}

// Edition metadata sourced from DeckService.latests
// This should match the data in src/lib/services/deckService.ts
const editionMetadata = [
  { 
    edition: 'mobileapp', 
    version: '1.1', 
    languages: ['en'],
    editionName: 'OWASP Cornucopia Mobile App Edition'
  },
  { 
    edition: 'webapp', 
    version: '2.2', 
    languages: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'],
    editionName: 'OWASP Cornucopia Website App Edition'
  }
];

function main() {
  for (const meta of editionMetadata) {
    const editionDir = path.join(buildDir, 'api', 'cre', meta.edition);
    // Ensure the edition directory exists
    fs.mkdirSync(editionDir, { recursive: true });
    
    // Write the edition metadata as index.html so static hosting
    // serves it when the directory URL is requested
    const outputFile = path.join(editionDir, 'index.html');
    const jsonContent = JSON.stringify({
      meta: {
        edition: meta.editionName,
        component: "cards",
        language: "en",
        languages: meta.languages,
        version: meta.version
      }
    });
    fs.writeFileSync(outputFile, jsonContent);
    console.log(`Generated edition metadata: ${outputFile}`);
  }
}

main();
