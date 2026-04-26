// Sync the UI toolkit CSS from the repo root into site/public so it's served
// statically. Runs automatically before `dev` and `build`.
import { copyFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = resolve(__dirname, '../../dist/ui-toolkit.min.css');
const destDir = resolve(__dirname, '../public');
const dest = resolve(destDir, 'ui-toolkit.min.css');

if (!existsSync(destDir)) mkdirSync(destDir, { recursive: true });
copyFileSync(src, dest);
console.log(`[sync-toolkit] ${src} → ${dest}`);
