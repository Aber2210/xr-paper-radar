// CDP smoke test for web/xr-paper-hub.html (Edge headless)
// Usage: node smoke_hub.mjs <port>
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const port = Number(process.argv[2] || 9333);
const edge = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const target = 'file:///D:/Agent/WorkBuddy/Research/web/xr-paper-hub.html';
const profile = path.join(os.tmpdir(), 'edge-smoke-' + port);

const proc = spawn(edge, [
  '--headless=new', `--remote-debugging-port=${port}`,
  `--user-data-dir=${profile}`, '--no-first-run', '--disable-gpu', target,
], { stdio: 'ignore' });

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function main() {
  // wait for devtools
  let ws = null;
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/list`);
      const tabs = await res.json();
      const page = tabs.find(t => t.type === 'page' && t.url.includes('xr-paper-hub'));
      if (page) { ws = page.webSocketDebuggerUrl; break; }
    } catch {}
    await sleep(250);
  }
  if (!ws) { console.error('FAIL: no devtools page target'); process.exit(1); }

  const WebSocket = (await import('node:worker_threads'), globalThis.WebSocket);
  const sock = new WebSocket(ws);
  await new Promise((res, rej) => { sock.onopen = res; sock.onerror = rej; });

  let id = 0;
  const pending = new Map();
  const errors = [];
  sock.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { res, rej } = pending.get(msg.id);
      pending.delete(msg.id);
      // exceptionDetails may be top-level (see project memory)
      if (msg.error) rej(new Error(JSON.stringify(msg.error)));
      else if (msg.result && msg.result.exceptionDetails) rej(new Error(JSON.stringify(msg.result.exceptionDetails)));
      else res(msg.result);
    } else if (msg.method === 'Runtime.exceptionThrown') {
      errors.push(msg.params.exceptionDetails.text + ' ' +
        (msg.params.exceptionDetails.exception?.description || ''));
    } else if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      errors.push('console.error: ' + msg.params.args.map(a => a.value ?? a.description ?? '').join(' '));
    }
  };
  const send = (method, params = {}) => new Promise((res, rej) => {
    const mid = ++id;
    pending.set(mid, { res, rej });
    sock.send(JSON.stringify({ id: mid, method, params }));
  });

  await send('Runtime.enable');
  await send('Page.enable');
  await sleep(2500); // let page settle

  const probe = await send('Runtime.evaluate', {
    expression: `(() => {
      const d = (typeof DATA !== 'undefined') ? DATA : null;
      const batchSel = document.querySelector('#batchSel, select');
      const optTexts = batchSel ? Array.from(batchSel.options).map(o => o.textContent) : [];
      return JSON.stringify({
        hasData: !!d,
        papers: d ? d.papers.length : -1,
        notes: d ? d.notes.length : -1,
        has1021: d ? d.papers.some(p => p.batch === '2026-10-21') : false,
        hasBF1021: d ? d.papers.some(p => p.batch === 'backfill-1021') : false,
        has1022: d ? d.papers.some(p => p.batch === '2026-10-22') : false,
        has1023: d ? d.papers.some(p => p.batch === '2026-10-23') : false,
        hasBF1023: d ? d.papers.some(p => p.batch === 'backfill-1023') : false,
        has1024: d ? d.papers.some(p => p.batch === '2026-10-24') : false,
        hasBF1024: d ? d.papers.some(p => p.batch === 'backfill-1024') : false,
        bodyLen: document.body ? document.body.innerHTML.length : -1,
        optTexts: optTexts.slice(-4)
      });
    })()`,
    returnByValue: true, awaitPromise: false,
  });
  const info = JSON.parse(probe.result.value);
  console.log('PROBE:', JSON.stringify(info, null, 1));
  console.log('PAGE_ERRORS:', errors.length ? errors.join('\\n') : 'none');
  const ok = info.hasData && info.papers === 618 && info.notes === 313 &&
             info.has1021 && info.hasBF1021 && info.has1022 && info.has1023 && info.hasBF1023 && info.has1024 && info.hasBF1024 &&
             info.bodyLen > 10000 && errors.length === 0;
  console.log(ok ? 'SMOKE: PASS' : 'SMOKE: FAIL');
  sock.close();
  proc.kill();
  process.exit(ok ? 0 : 1);
}

main().catch(e => { console.error('FAIL:', e.message); proc.kill(); process.exit(1); });
