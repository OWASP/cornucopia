import fs from 'fs';
import path from 'path';
import process from 'process';

const __dirname = path.resolve();
let buildDir = '';
if (fs.existsSync(path.join(__dirname, 'build'))) {
  buildDir = path.join(__dirname, 'build');
} else if (fs.existsSync(path.join(__dirname, 'output'))) {
  buildDir = path.join(__dirname, 'output');
} else {
  process.exit(0);
}

// Copying the file to a the same name
fs.copyFile("./src/404.html", buildDir + "/404.html", 
      fs.constants.COPYFILE_EXCL, (err) => {
  if (err) {
    console.log("Error Found:", err);
  }
});
