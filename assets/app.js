'use strict';
const $ = id => document.getElementById(id);
const safe = value => value === null || value === undefined || value === '' ? '—' : String(value);
const dateText = value => { if (!value) return '—'; const d = new Date(value); return isNaN(d.getTime()) ? '—' : d.toLocaleString(); };


function repoActionsURL() {
  const segments = location.pathname.split('/').filter(Boolean);
  const repo = segments.length && !location.hostname.endsWith('.github.io') ? null : segments[0];
  if (!location.hostname.endsWith('.github.io')) return null;
  const owner = location.hostname.split('.')[0];
  const name = repo || `${owner}.github.io`;
  return `https://github.com/${encodeURIComponent(owner)}/${encodeURIComponent(name)}/actions/workflows/scan.yml`;
}

function setText(id, value) { $(id).textContent = safe(value); }
function showLatest(data) {
  setText('status', data.status); $('status').className = 'metric-value ' + (data.status === 'PASS' ? 'good' : 'bad');
  setText('http', data.http_status); setText('speed', data.load_seconds == null ? '—' : data.load_seconds + 's');
  setText('broken', Array.isArray(data.broken_links) ? data.broken_links.length : 0);
  setText('links', data.links_checked || 0); setText('requested', data.requested_url);
  setText('final-url', data.final_url); setText('title', data.title);
  setText('checked', dateText(data.checked_at)); setText('updated', 'Last run: ' + dateText(data.checked_at));
  setText('error', data.error || (Array.isArray(data.broken_links) && data.broken_links.length ? data.broken_links.map(x => `${x.status}: ${x.url}`).join(' | ') : 'None reported'));
  setText('result-badge', data.status === 'PASS' ? 'All checks passed' : 'Issues detected');
  if (data.screenshot) { $('screenshot').src = 'data/latest.png?v=' + Date.now(); $('screenshot').hidden = false; $('shot-placeholder').hidden = true; }
}

function showHistory(items) {
  const body = $('history-body'); body.replaceChildren();
  if (!Array.isArray(items) || !items.length) { const tr = body.insertRow(); const td = tr.insertCell(); td.colSpan = 5; td.className = 'empty'; td.textContent = 'No scan history yet.'; return; }
  for (const item of items) {
    const row = body.insertRow();
    for (const value of [item.requested_url, dateText(item.checked_at), item.status, item.http_status, item.load_seconds == null ? '—' : item.load_seconds + 's']) {
      const cell = row.insertCell(); cell.textContent = safe(value);
      if (value === 'PASS') cell.className = 'good'; if (value === 'FAIL') cell.className = 'bad';
    }
  }
}

async function loadData() {
  try { const response = await fetch('data/latest.json?ts=' + Date.now(), { cache: 'no-store' }); if (response.ok) { const data = await response.json(); if (data && data.checked_at) showLatest(data); } } catch (e) { console.info('No scan data available yet.'); }
  try { const response = await fetch('data/history.json?ts=' + Date.now(), { cache: 'no-store' }); if (response.ok) showHistory(await response.json()); } catch (e) { console.info('No history available yet.'); }
}

$('scan-form').addEventListener('submit', event => {
  event.preventDefault();
  const url = $('site-url').value.trim();
  try { const parsed = new URL(url); if (!['https:', 'http:'].includes(parsed.protocol)) throw Error('Invalid protocol'); }
  catch (e) { alert('Enter a valid URL beginning with https:// or http://'); return; }
  const instructions = $('scan-instructions'); instructions.replaceChildren();
  const heading = document.createElement('strong'); heading.textContent = 'Ready to scan: ' + url; instructions.append(heading);
  const steps = document.createElement('div'); steps.textContent = 'Open GitHub Actions → Run workflow → paste the URL into the website field → Run workflow. Once it finishes, refresh this dashboard.'; instructions.append(steps);
  const actions = repoActionsURL();
  if (actions) { const link = document.createElement('a'); link.href = actions; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = 'Open Run Website Scan on GitHub ↗'; instructions.append(link); }
  else { const note = document.createElement('div'); note.textContent = 'After publishing to GitHub Pages, the Actions link will appear here.'; instructions.append(note); }
  const copy = document.createElement('button'); copy.className = 'secondary-button'; copy.type = 'button'; copy.textContent = 'Copy URL'; copy.style.marginLeft = '12px'; copy.onclick = () => navigator.clipboard?.writeText(url); instructions.append(copy);
  instructions.hidden = false;
});

$('refresh').addEventListener('click', loadData);
loadData();
