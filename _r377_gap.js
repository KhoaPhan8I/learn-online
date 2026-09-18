// Refined gap analysis: functions never referenced inside any T('...') body.
const fs = require('fs');
const s = fs.readFileSync('index.html', 'utf-8').replace(/^﻿/, '');
const fnRe = /function ([A-Za-z0-9_$]+)\(/g;
const fns = new Set();
let m;
while ((m = fnRe.exec(s))) fns.add(m[1]);
// collect test bodies: T('name', BODY); — bodies are single-line IIFEs here
const tRe = /T\('[^']+',([\s\S]*?)\)\);/g;
let bodies = '';
while ((m = tRe.exec(s))) bodies += m[1] + '\n';
const uncovered = [...fns].filter(f => {
  if (f.length < 4) return false;
  const re = new RegExp('\\b' + f + '\\b');
  return !re.test(bodies);
});
console.log('total fns:', fns.size);
console.log('--- truly uncovered (' + uncovered.length + ') ---');
uncovered.forEach(f => console.log(f));
