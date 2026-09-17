
const fs = require('fs');
const file = process.argv[2];
const content = fs.readFileSync(file, 'utf8');

// Match script tags
const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
let errors = 0;

while ((match = scriptRegex.exec(content)) !== null) {
  count++;
  const scriptContent = match[1].trim();
  const typeMatch = match[0].match(/type=["']([^"']+)["']/i);
  const type = typeMatch ? typeMatch[1] : 'text/javascript';

  if (type === 'application/ld+json' || type === 'application/json' || type === 'speculationrules') {
    if (!scriptContent) continue;
    try {
      JSON.parse(scriptContent);
    } catch(e) {
      console.log(`[JSON Error] ${file} script #${count}: ${e.message}`);
      errors++;
    }
  } else if (type.includes('javascript') || type === 'text/javascript' || !typeMatch) {
    if (!scriptContent) continue;
    try {
      new Function(scriptContent);
    } catch(e) {
      console.log(`[JS Error] ${file} script #${count}: ${e.message}`);
      errors++;
    }
  }
}
if (errors === 0) {
  console.log(`No script errors in ${file}`);
}
