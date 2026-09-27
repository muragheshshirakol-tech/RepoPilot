import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDir, "..", "frontend");

// Resolve TypeScript from the frontend's own node_modules.
const require = createRequire(
  pathToFileURL(path.join(root, "package.json"))
);
const ts = require("typescript");

const extensions = new Set([".ts", ".tsx"]);
const ignored = new Set(["node_modules", ".next", ".vercel"]);
const files = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (ignored.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (extensions.has(path.extname(entry.name))) files.push(full);
  }
}

function formatDiagnostic(diagnostic) {
  const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, "\n");
  if (diagnostic.file && typeof diagnostic.start === "number") {
    const pos = diagnostic.file.getLineAndCharacterOfPosition(diagnostic.start);
    return `${path.relative(process.cwd(), diagnostic.file.fileName)}:${pos.line + 1}:${pos.character + 1}: ${message}`;
  }
  return message;
}

walk(root);
for (const file of files) {
  const source = fs.readFileSync(file, "utf8");
  const ext = path.extname(file);
  const kind = ext === ".tsx" ? ts.ScriptKind.TSX : ts.ScriptKind.TS;
  const sf = ts.createSourceFile(file, source, ts.ScriptTarget.Latest, true, kind);
  const diagnostics = sf.parseDiagnostics ?? [];
  if (diagnostics.length) throw new Error(formatDiagnostic(diagnostics[0]));
}

console.log(`Frontend TypeScript/TSX syntax PASS (${files.length} files parsed)`);
