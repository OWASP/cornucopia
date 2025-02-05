import fs from 'fs';
import path from 'path';
import process from 'process';

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


function main() {
  const headers = `/*
  Access-Control-Allow-Origin: https://cornucopia.owasp.org
  Cross-Origin-Embedder-Policy: require-corp
  Cross-Origin-Opener-Policy: same-origin
  X-Frame-Options: SAMEORIGIN
  X-XSS-Protection: 1; mode=block
  X-Content-Type-Options: nosniff
  Referrer-Policy: same-origin
  Permissions-Policy: accelerometer=(), autoplay=(), camera=(), document-domain=(), encrypted-media=(), fullscreen=(self "https://www.youtube.com/"), gyroscope=(), interest-cohort=(), magnetometer=(), microphone=(), midi=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), sync-xhr=(), usb=(), xr-spatial-tracking=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: base-uri 'self'; default-src 'none'; frame-src 'self' https://www.youtube.com/; connect-src 'self'; img-src 'self' https://i.ytimg.com/vi/XXTPXozIHow/mqdefault.jpg; script-src 'self' 'nonce-DhcnhD3khTMePgXw'; style-src 'self'; style-src-elem 'self'; upgrade-insecure-requests

/how-to-play
  ! Permissions-Policy
  Permissions-Policy: accelerometer=(), autoplay=(), camera=(), document-domain=(), encrypted-media=(), fullscreen=(self "https://www.youtube.com/"), gyroscope=(), interest-cohort=(), magnetometer=(), microphone=(), midi=(), payment=(), picture-in-picture=(self "https://www.youtube.com/"), publickey-credentials-get=(), sync-xhr=(), usb=(), xr-spatial-tracking=(), geolocation=()
`;

  const headersFile = path.join(buildDir, '_headers');
  fs.writeFileSync(headersFile, headers);
}

main();