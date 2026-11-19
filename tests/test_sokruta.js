// Krav: K28 i KRAV.md, beslut 0018. Kör docs/sokning.js och docs/sokruta.js mot en liten
// påhittad sida och ett påhittat sökindex: node --test tests/*.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const las = (namn) => fs.readFileSync(path.join(__dirname, "..", "docs", namn), "utf8");
const SKRIPT = las("sokning.js") + "\n" + las("sokruta.js");

const INDEX = {
  foreningar: { "Förening Åsa": ["Åsa"], "Förening Särö": ["Särö"] },
  arenden: [
    { rubrik: "Detaljplan Stockalid 1:4", adress: "arende/a.html", orter: ["Åsa"], status: "pågår",
      kallas: ["Stockalidshusen"], traff: "detaljplan stockalid 1:4 åsa stockalidshusen", text: "" },
    { rubrik: "Åsa station", adress: "arende/b.html", orter: ["Åsa"], status: "pågår",
      kallas: [], traff: "åsa station åsa", text: "stockalid 1:9 berörs." },
    { rubrik: "Stockalid i Särö", adress: "arende/c.html", orter: ["Särö"], status: "klart",
      kallas: [], traff: "stockalid i särö särö", text: "" },
  ],
  motet: { rubrik: "KS-mötet 24 november 2026", punkter: [
    { rubrik: "Avtal Stockalid", adress: "ks-motet.html#punkt-9", nummer: 9, dnr: "KS-2021-01226",
      traff: "avtal stockalid ks-2021-01226", text: "" },
  ] },
};

// Ett element med just det skripten använder.
class El {
  constructor(tagg, attribut = {}, barn = []) {
    Object.assign(this, { tagg, attribut, barn: [], lyssnare: {}, hidden: false, text: "", value: "" });
    barn.forEach((b) => this.appendChild(b));
  }
  set textContent(t) { this.barn = []; this.text = t; }
  get textContent() { return this.text + this.barn.map((b) => b.textContent).join(""); }
  setAttribute(namn, varde) { this.attribut[namn] = String(varde); }
  getAttribute(namn) { return namn in this.attribut ? this.attribut[namn] : null; }
  set className(k) { this.attribut.class = k; }
  appendChild(b) { b.parentNode = this; this.barn.push(b); return b; }
  insertBefore(b, fore) { b.parentNode = this; this.barn.splice(this.barn.indexOf(fore), 0, b); return b; }
  focus() { El.fokus = this; }
  addEventListener(typ, fn) { (this.lyssnare[typ] = this.lyssnare[typ] || []).push(fn); }
  skicka(typ, handelse = {}) { (this.lyssnare[typ] || []).forEach((fn) => fn(handelse)); }
  efterkommande() { return this.barn.flatMap((b) => [b, ...(b.efterkommande ? b.efterkommande() : [])]); }
  passar(valjare) {
    if (valjare.startsWith(".")) return (this.attribut.class || "").split(" ").includes(valjare.slice(1));
    const [namn, varde] = valjare.slice(1, -1).split("=");
    if (valjare.startsWith("[")) return varde === undefined ? namn in this.attribut : this.attribut[namn] === varde;
    return this.tagg === valjare;
  }
  querySelectorAll(valjare) { return this.efterkommande().filter((e) => e.passar && e.passar(valjare)); }
  querySelector(valjare) { return this.querySelectorAll(valjare)[0] || null; }
}

const vanta = () => new Promise((klar) => setImmediate(klar));

function sida({ oppen = false, svar = { ok: true, json: () => INDEX }, fraga = "" } = {}) {
  const tema = new El("button", { class: "temaknapp" });
  const rad = new El("nav", { class: "sajtrad" }, [new El("div", {}, [new El("ul"), tema, new El("button", { class: "menyknapp" })])]);
  const meny = new El("nav", { class: "sajtmeny" });
  const main = new El("main", {}, oppen ? [new El("ul", { "data-sok-oppen": "" })] : []);
  const kropp = new El("body", {}, [rad, meny, main]);
  const hamtat = [];
  const document = Object.assign(kropp, {
    createElement: (tagg) => new El(tagg),
    createTextNode: (text) => ({ textContent: text }),
    currentScript: new El("script", { src: "../sokruta.js" }),
  });
  const fetch = (adress) => { hamtat.push(adress); return Promise.resolve(svar); };
  vm.runInNewContext(SKRIPT, { document, fetch, URLSearchParams, location: { search: fraga } });
  const knapp = kropp.querySelector(".sokknapp");
  const panel = kropp.querySelector(".sokpanel");
  const falt = panel.querySelector("input");
  const skriv = async (text) => { falt.value = text; falt.skicka("input"); await vanta(); };
  return { kropp, rad, tema, knapp, panel, falt, skriv, hamtat };
}

const rubriker = (panel) => panel.querySelectorAll("h2").map((h) => h.textContent);
const lankar = (panel) => panel.querySelectorAll("a").map((a) => a.getAttribute("href"));
const smatt = (panel) => panel.querySelectorAll("small").map((s) => s.textContent);

test("knappen står före temaknappen och fäller ut fältet, som hämtar indexet en gång", async () => {
  const { kropp, rad, tema, knapp, panel, falt, hamtat } = sida();
  const div = rad.querySelector("div");
  assert.strictEqual(div.barn.indexOf(knapp), div.barn.indexOf(tema) - 1);
  assert.strictEqual(kropp.barn.indexOf(panel), 1);
  assert.deepStrictEqual([knapp.textContent, panel.hidden], ["Sök", true]);
  knapp.skicka("click");
  await vanta();
  assert.deepStrictEqual([knapp.getAttribute("aria-expanded"), panel.hidden, El.fokus], ["true", false, falt]);
  knapp.skicka("click");
  knapp.skicka("click");
  await vanta();
  assert.deepStrictEqual(hamtat, ["../sok.json"]);
});

test("träffarna i grupper med antal, urvalet i länken och märkningen", async () => {
  const { knapp, panel, skriv } = sida({ fraga: "?forening=F%C3%B6rening%20%C3%85sa" });
  knapp.skicka("click");
  await skriv("Stockalid");
  assert.deepStrictEqual(rubriker(panel), ["Ärenden i Förening Åsa (2)", "KS-mötet 24 november 2026 (1)"]);
  assert.deepStrictEqual(lankar(panel), [
    "../arende/a.html?forening=F%C3%B6rening%20%C3%85sa",
    "../arende/b.html?forening=F%C3%B6rening%20%C3%85sa",
    "../ks-motet.html#punkt-9",
  ]);
  assert.deepStrictEqual(smatt(panel), [
    "Åsa · pågår · uppmärksammat som Stockalidshusen",
    "Åsa · pågår · nämns i texten",
    "Punkt 9 · Dnr KS-2021-01226",
  ]);
  assert.strictEqual(panel.querySelectorAll("mark")[0].textContent, "Stockalid");
  assert.strictEqual(panel.querySelector("[role=status]").textContent, "3 träffar");
});

test("ett tecken söker inte, och utan träff står det", async () => {
  const { knapp, panel, skriv } = sida();
  knapp.skicka("click");
  await skriv("s");
  assert.deepStrictEqual([rubriker(panel), panel.querySelector("[role=status]").textContent], [[], ""]);
  await skriv("ingenting");
  assert.strictEqual(panel.querySelector("[role=status]").textContent, "Inga träffar.");
});

test("Escape fäller ihop fältet och lämnar fokus på knappen", () => {
  const { knapp, panel } = sida();
  knapp.skicka("click");
  let stoppad = false;
  panel.skicka("keydown", { key: "Escape", stopPropagation: () => { stoppad = true; } });
  assert.deepStrictEqual([panel.hidden, knapp.getAttribute("aria-expanded"), El.fokus], [true, "false", knapp]);
  assert.ok(stoppad, "menyns Escape i sajter.js ska inte också köras");
});

test("på sidan Sök är fältet utfällt från början, utan att ta fokus", () => {
  El.fokus = null;
  const { panel, knapp } = sida({ oppen: true });
  assert.deepStrictEqual([panel.hidden, knapp.getAttribute("aria-expanded"), El.fokus], [false, "true", null]);
});

test("gick indexet inte att ladda står det, och nästa sökning försöker igen", async () => {
  const { knapp, panel, skriv, hamtat } = sida({ svar: { ok: false, status: 404 } });
  knapp.skicka("click");
  await vanta();
  assert.strictEqual(panel.querySelector("[role=status]").textContent, "Sökningen gick inte att ladda.");
  await skriv("stockalid");
  assert.strictEqual(hamtat.length, 2);
});
