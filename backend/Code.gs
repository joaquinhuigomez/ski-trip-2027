/**
 * Ski Trip 2027 — vote backend (Google Apps Script web app).
 * Deploy: Deploy > New deployment > Web app > Execute as: Me > Who has access: Anyone.
 * Storage: a Google Sheet auto-created in the owner's Drive on first request.
 * Each POST appends a row; GET returns the latest ballot per person plus the comment feed.
 */
const ALLOWED_NAMES = ['Joaquin', 'Juan', 'Chloe', 'Kannes', 'Ina', 'Natasha'];
const MAX_PAYLOAD_CHARS = 20000;
const MAX_COMMENT_CHARS = 1000;
const SHEET_NAME = 'votes';

function getSheet_() {
  const props = PropertiesService.getScriptProperties();
  let id = props.getProperty('SHEET_ID');
  let ss;
  if (id) {
    ss = SpreadsheetApp.openById(id);
  } else {
    ss = SpreadsheetApp.create('Ski Trip Jan 2027 — votes');
    props.setProperty('SHEET_ID', ss.getId());
  }
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.getSheets()[0];
    sh.setName(SHEET_NAME);
    sh.appendRow(['timestamp', 'name', 'type', 'answers_json', 'comment']);
    sh.setFrozenRows(1);
  }
  return sh;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function readState_() {
  const rows = getSheet_().getDataRange().getValues().slice(1);
  const latest = {};
  const comments = [];
  rows.forEach(function (r) {
    const ts = r[0] instanceof Date ? r[0].toISOString() : String(r[0]);
    const name = String(r[1]);
    const type = String(r[2]);
    if (type === 'ballot') {
      let answers = {};
      try { answers = JSON.parse(r[3] || '{}'); } catch (e) { answers = {}; }
      latest[name] = { name: name, ts: ts, answers: answers };
    }
    if (r[4]) comments.push({ name: name, ts: ts, text: String(r[4]) });
  });
  return { ok: true, ballots: Object.keys(latest).map(function (k) { return latest[k]; }), comments: comments };
}

function doGet() {
  return json_(readState_());
}

function doPost(e) {
  const raw = (e && e.postData && e.postData.contents) || '';
  if (raw.length > MAX_PAYLOAD_CHARS) return json_({ ok: false, error: 'payload_too_large' });
  let body;
  try { body = JSON.parse(raw); } catch (err) { return json_({ ok: false, error: 'bad_json' }); }
  const name = String(body.name || '');
  if (ALLOWED_NAMES.indexOf(name) === -1) return json_({ ok: false, error: 'unknown_name' });
  const type = body.type === 'comment' ? 'comment' : 'ballot';
  const comment = String(body.comment || '').slice(0, MAX_COMMENT_CHARS);
  const answers = type === 'ballot' ? JSON.stringify(body.answers || {}) : '';
  if (type === 'comment' && !comment.trim()) return json_({ ok: false, error: 'empty_comment' });

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    getSheet_().appendRow([new Date(), name, type, answers, comment]);
  } finally {
    lock.releaseLock();
  }
  return json_(readState_());
}

/** Run once from the editor to trigger the authorization prompt and create the Sheet. */
function setup() {
  Logger.log('Sheet: ' + getSheet_().getParent().getUrl());
}
