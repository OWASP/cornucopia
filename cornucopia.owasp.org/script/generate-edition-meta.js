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

const editions = {
  webapp: {
    edition: "OWASP Cornucopia Website App Edition",
    component: "cards",
    language: "all",
    languages: ["en", "es", "fr", "nl", "no_nb", "pt_br", "pt_pt", "it", "ru"],
    version: "2.2"
  },
  mobileapp: {
    edition: "OWASP Cornucopia Mobile App Edition",
    component: "cards",
    language: "all",
    languages: ["en"],
    version: "1.1"
  }
};

function main() {
  for (const [editionKey, meta] of Object.entries(editions)) {
    const editionDir = path.join(buildDir, 'api', 'cre', editionKey);
    // Ensure the edition directory exists
    fs.mkdirSync(editionDir, { recursive: true });
    // Write the edition metadata as index.html so static hosting
    // serves it when the directory URL is requested
    const outputFile = path.join(editionDir, 'index.html');
    const jsonContent = JSON.stringify({ meta });
    fs.writeFileSync(outputFile, jsonContent);
    console.log(`Generated edition metadata: ${outputFile}`);
  }
}

main();
