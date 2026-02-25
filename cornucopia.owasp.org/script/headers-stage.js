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
  Access-Control-Allow-Origin: https://owaspcornucopia.org
  Cross-Origin-Opener-Policy: same-origin
  X-Robots-Tag: noindex
  X-Frame-Options: SAMEORIGIN
  X-XSS-Protection: 1; mode=block
  X-Content-Type-Options: nosniff
  Referrer-Policy: same-origin
  Permissions-Policy: accelerometer=(), autoplay=(), camera=(), document-domain=(), encrypted-media=(), fullscreen=(self "https://www.youtube.com/"), gyroscope=(), interest-cohort=(), magnetometer=(), microphone=(), midi=(), payment=(), picture-in-picture=(self "https://www.youtube.com/"), publickey-credentials-get=(), sync-xhr=(), usb=(), xr-spatial-tracking=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: base-uri 'self'; default-src 'none'; frame-src 'self' www.youtube.com youtube.com; connect-src 'self'; img-src 'self' i.ytimg.com; script-src 'self' 'nonce-DhcnhD3khTMePgXw'; style-src 'self'; style-src-elem 'self'; upgrade-insecure-requests
/api/cre/mobileapp
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/mobileapp/en
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/en
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/es
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/fr
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/nl
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/no_nb
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/it
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/pt_pt
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/pt_br
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
/api/cre/webapp/ru
  ! Access-Control-Allow-Origin
  Access-Control-Allow-Origin: *
  ! Content-Type
  Content-Type: application/json
`;

  const headersFile = path.join(buildDir, '_headers');
  fs.writeFileSync(headersFile, headers);
}

main();
