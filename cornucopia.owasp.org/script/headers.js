import { getBuildDir, writeHeaders } from './headers-common.js';

const buildDir = getBuildDir();

if (buildDir) {
  writeHeaders({
    buildDir,
    origin: 'https://cornucopia.owasp.org',
    includeNotFound: true
  });
}
