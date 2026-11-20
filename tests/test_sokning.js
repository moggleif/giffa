// Krav: K28 i KRAV.md, beslut 0018. Kör docs/sokning.js med påhittade poster:
// node --test tests/*.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const SKRIPT = fs.readFileSync(path.join(__dirname, "..", "docs", "sokning.js"), "utf8");
const omfang = {};
vm.runInNewContext(SKRIPT, omfang);
const S = omfang.Sokning;

const post = (rubrik, traff, text, orter = ["Åsa"]) => ({ rubrik, traff, text, orter, kallas: [] });
const POSTER = [
  post("Planprogram för Åsa station", "planprogram för åsa station åsa", "stockalid 1:9 berörs."),
  post("Detaljplan Stockalid 1:4", "detaljplan stockalid 1:4 åsa ks-2021-01226", "bostäder och förskola."),
  post("Förskola i Särö", "förskola i särö särö", "", ["Särö"]),
];
// vm-kontextens listor har en annan Array-prototyp; JSON gör dem jämförbara.
const vanlig = (varde) => JSON.parse(JSON.stringify(varde));
const rubriker = (traffar) => vanlig(traffar).map((t) => t.post.rubrik + (t.iTexten ? " (text)" : ""));

test("orden i små bokstäver utan tomma", () => {
  assert.deepStrictEqual(vanlig(S.orden("  Stockalid   ÅSA ")), ["stockalid", "åsa"]);
});

test("varje ord ska finnas; träff utanför texten först, de andra märkta", () => {
  assert.deepStrictEqual(rubriker(S.traffar(POSTER, S.orden("Stockalid"))),
    ["Detaljplan Stockalid 1:4", "Planprogram för Åsa station (text)"]);
  assert.deepStrictEqual(rubriker(S.traffar(POSTER, S.orden("förskola ks-2021"))),
    ["Detaljplan Stockalid 1:4 (text)"]);
  assert.deepStrictEqual(rubriker(S.traffar(POSTER, S.orden("särö åsa"))), []);
});

test("urvalet: en ort, en förening, en ort i föreningen, och ogiltigt ger inget urval", () => {
  const foreningar = { "Förening Åsa": ["Åsa", "Fjärås"], "Förening Särö": ["Särö"] };
  assert.deepStrictEqual(vanlig(S.urvalet(foreningar, null, "Särö")), { namn: "Särö", orter: ["Särö"] });
  assert.deepStrictEqual(vanlig(S.urvalet(foreningar, "Förening Åsa", null)),
    { namn: "Förening Åsa", orter: ["Åsa", "Fjärås"] });
  assert.deepStrictEqual(vanlig(S.urvalet(foreningar, "Förening Åsa", "Särö")),
    { namn: "Förening Åsa", orter: ["Åsa", "Fjärås"] });
  assert.strictEqual(S.urvalet(foreningar, "toString", "Ingenstans"), null);
  const iSaro = S.iUrvalet(POSTER, S.urvalet(foreningar, null, "Särö"));
  assert.deepStrictEqual(iSaro.map((p) => p.rubrik), ["Förskola i Särö"]);
  assert.strictEqual(S.iUrvalet(POSTER, null).length, 3);
});

test("orden markeras i rubriken, oavsett stora och små bokstäver", () => {
  assert.deepStrictEqual(vanlig(S.delar("Detaljplan Stockalid 1:4", S.orden("stockalid 1"))),
    [["Detaljplan ", false], ["Stockalid", true], [" ", false], ["1", true], [":4", false]]);
  assert.deepStrictEqual(vanlig(S.delar("Åsa station", S.orden("åsa å"))), [["Åsa", true], [" station", false]]);
  assert.deepStrictEqual(vanlig(S.delar("Ingen träff", ["x"])), [["Ingen träff", false]]);
});

test("namnen som något ord finns i", () => {
  const p = Object.assign(post("Höglager", "", ""), { kallas: ["Jättelagret i Frillesås", "Annat"] });
  assert.deepStrictEqual(vanlig(S.namnen(p, S.orden("jättelagret"))), ["Jättelagret i Frillesås"]);
});
