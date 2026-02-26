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

/**
 * Returns the default edition metadata currently used by this script.
 * This serves as a secure fallback if no shared metadata file is present
 * or if that file cannot be parsed safely.
 * 
 * ASVS V16.5: Fail securely by using a known-good default on errors.
 */
function getDefaultEditions() {
  return {
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
}

/**
 * Attempts to load edition metadata from a shared JSON file so that
 * metadata is defined in a single source of truth.
 * 
 * If the shared file does not exist or is invalid, this function falls
 * back to the hardcoded defaults returned by getDefaultEditions().
 * 
 * The expected JSON structure is an object with keys like "webapp",
 * "mobileapp", etc., mirroring the default structure.
 */
function loadEditions() {
  // Place a shared metadata file alongside the repository root or adjust
  // this path consistently across consumers to avoid drift.
  const sharedMetaPath = path.join(__dirname, 'editions-meta.json');
  
  if (!fs.existsSync(sharedMetaPath)) {
    return getDefaultEditions();
  }
  
  try {
    const raw = fs.readFileSync(sharedMetaPath, { encoding: 'utf8' });
    const parsed = JSON.parse(raw);
    
    // Basic structural validation: ensure we have a plain object.
    if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
      return parsed;
    }
    
    // If structure is not as expected, fall back to defaults.
    console.error('Shared editions-meta.json has an unexpected structure; using default editions.');
    return getDefaultEditions();
  } catch (error) {
    // Avoid exposing internal details; log a generic message.
    // ASVS V16.5: Do not leak sensitive information in error messages.
    console.error('Unable to read or parse editions-meta.json; using default editions.');
    return getDefaultEditions();
  }
}

const editions = loadEditions();

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
