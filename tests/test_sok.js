// Krav: K28 i KRAV.md. Kör docs/sok.js mot en liten påhittad sida: node --test tests/*.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const SKRIPT = fs.readFileSync(path.join(__dirname, "..", "docs", "sok.js"), "utf8");

function nod(attribut = {}) {
  return {
    attribut, hidden: false, lyssnare: [],
    getAttribute(namn) { return this.attribut[namn]; },
    addEventListener(_typ, fn) { this.lyssnare.push(fn); },
  };
}

function sida() {
  const rutan = Object.assign(nod(), { hidden: true });
  const falt = Object.assign(nod(), { value: "", parentNode: rutan });
  const poster = ["detaljplan åsa 5:156 restaurangstråket i åsa åsa", "lagret frillesås", "säröhus särö"]
    .map((text) => nod({ "data-sok": text }));
  const ingen = Object.assign(nod(), { hidden: true });
  const document = {
    getElementById: (id) => (id === "sok" ? falt : null),
    querySelectorAll: () => poster,
    querySelector: () => ingen,
  };
  vm.runInNewContext(SKRIPT, { document });
  const sok = (varde) => { falt.value = varde; falt.lyssnare.forEach((fn) => fn()); };
  const synliga = () => poster.filter((p) => !p.hidden).map((p) => p.getAttribute("data-sok").split(" ")[0]);
  return { rutan, ingen, sok, synliga };
}

test("rutan syns och utan ord syns alla ärenden", () => {
  const { rutan, synliga, ingen } = sida();
  assert.strictEqual(rutan.hidden, false);
  assert.deepStrictEqual(synliga(), ["detaljplan", "lagret", "säröhus"]);
  assert.strictEqual(ingen.hidden, true);
});

test("varje ord ska finnas, utan hänsyn till stora och små bokstäver", () => {
  const { sok, synliga } = sida();
  sok("Restaurangstråket ÅSA");
  assert.deepStrictEqual(synliga(), ["detaljplan"]);
  sok("  särö ");
  assert.deepStrictEqual(synliga(), ["säröhus"]);
});

test("utan träff står det", () => {
  const { sok, synliga, ingen } = sida();
  sok("lagret särö");
  assert.deepStrictEqual(synliga(), []);
  assert.strictEqual(ingen.hidden, false);
});
