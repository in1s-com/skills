#!/usr/bin/env node
// Compares skills/in1s/references/tool-map.md with the tools the in1s MCP server actually offers.
//
//   IN1S_TOKEN=in1s_... node scripts/check-tool-map.mjs
//
// Use a site token made with "Everything your role allows" by a website owner, so the server lists every tool.
// A narrower token lists fewer tools, and the check reports those as "in the map, not offered" without failing.
// Optional: IN1S_MCP_URL (default https://accounts.in1s.com/mcp).
//
// Exits 1 when the server offers a tool the map does not mention.

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const endpoint = process.env.IN1S_MCP_URL || 'https://accounts.in1s.com/mcp';
const token = process.env.IN1S_TOKEN;

if (!token) {
  console.error('Set IN1S_TOKEN to an in1s site token (in1s_...).');
  process.exit(2);
}

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const mapText = await readFile(join(root, 'skills/in1s/references/tool-map.md'), 'utf8');

/** The backticked names in the first column of each table row; names with * are kept as patterns. */
const mentioned = new Set();
const patterns = [];
for (const line of mapText.split('\n')) {
  const firstCell = line.match(/^\|\s*(`[^|]*)\|/)?.[1];
  if (!firstCell) continue;
  for (const [, name] of firstCell.matchAll(/`([a-z*][a-z0-9_*]*)`/g)) {
    if (name.includes('*')) patterns.push(new RegExp(`^${name.replaceAll('*', '[a-z0-9_]*')}$`));
    else mentioned.add(name);
  }
}

async function rpc(method, params, id) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      Accept: 'application/json, text/event-stream',
    },
    body: JSON.stringify({ jsonrpc: '2.0', id, method, params }),
  });
  if (!response.ok) {
    throw new Error(`${method}: HTTP ${response.status} ${await response.text()}`);
  }
  const text = await response.text();
  // A streamable-HTTP server may answer as an event stream: take the JSON of its data line.
  const json = text.trimStart().startsWith('{') ? text : text.split('\n').find((line) => line.startsWith('data:'))?.slice(5);
  const message = JSON.parse(json);
  if (message.error) throw new Error(`${method}: ${message.error.message}`);
  return message.result;
}

const offered = [];
let cursor;
let id = 1;
do {
  const result = await rpc('tools/list', cursor ? { cursor } : {}, id++);
  offered.push(...result.tools.map((tool) => tool.name));
  cursor = result.nextCursor;
} while (cursor);

const covered = (name) => mentioned.has(name) || patterns.some((pattern) => pattern.test(name));
const missingFromMap = offered.filter((name) => !covered(name)).sort();
const offeredSet = new Set(offered);
const notOffered = [...mentioned].filter((name) => !offeredSet.has(name)).sort();

console.log(`Server offers ${offered.length} tools; the map names ${mentioned.size} (+ ${patterns.length} patterns).`);
if (notOffered.length) {
  console.log(`\nIn the map, not offered to this token (fine for a narrow token; check with an owner token):`);
  for (const name of notOffered) console.log(`  ${name}`);
}
if (missingFromMap.length) {
  console.log(`\nOffered by the server, missing from tool-map.md:`);
  for (const name of missingFromMap) console.log(`  ${name}`);
  process.exit(1);
}
console.log('\ntool-map.md covers every tool the server offers.');
