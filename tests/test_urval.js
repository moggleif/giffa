// Krav: K21 och K22 i KRAV.md, issue #35. Kör docs/urval.js mot en liten
// påhittad sida med standardbibliotekets testlöpare: node --test tests/*.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const SKRIPT = fs.readFileSync(path.join(__dirname, "..", "docs", "urval.js"), "utf8");
const VALJARE = /^(\w+)?(?:\.([\w-]+))?(?:\[([\w-]+)\])?$/;

// En nod med just det urval.js använder: attribut, hidden, barn och klick.
class Nod {
  constructor(tagg, attribut = {}, barn = [], hidden = false) {
    Object.assign(this, { tagg, attribut, barn, hidden, lyssnare: [] });
  }
  getAttribute(namn) { return namn in this.attribut ? this.attribut[namn] : null; }
  hasAttribute(namn) { return namn in this.attribut; }
  setAttribute(namn, varde) { this.attribut[namn] = String(varde); }
  addEventListener(_typ, fn) { this.lyssnare.push(fn); }
  click() { this.lyssnare.forEach((fn) => fn()); }
  passar(valjare) {
    const [, tagg, klass, attribut] = VALJARE.exec(valjare);
    const klasser = (this.getAttribute("class") || "").split(" ");
    return (!tagg || tagg === this.tagg) && (!klass || klasser.includes(klass)) &&
      (!attribut || this.hasAttribute(attribut));
  }
  querySelectorAll(valjare) {
    return this.barn.flatMap((b) => (b.passar(valjare) ? [b] : []).concat(b.querySelectorAll(valjare)));
  }
  querySelector(valjare) { return this.querySelectorAll(valjare)[0] || null; }
}

const knapp = (attribut) => new Nod("button", attribut);
const grupp = (forening, orter) => new Nod("div", { "data-urval-grupp": forening },
  orter.map((ort) => knapp({ "data-urval-ort": ort })), true);
const sak = (orter) => new Nod("li", { "data-ort": orter });
const lista = (saker) => new Nod("div", { class: "urvalslista" }, [
  new Nod("table", { class: "tabell" }), ...saker, new Nod("p", { class: "inget-val" }, [], true),
]);

// Förening A har orterna x och y, förening B orten z. Den andra listan har bara y.
function sida(sok) {
  const dokument = new Nod("html", {}, [
    new Nod("div", { class: "urval" }, [
      knapp({ "data-alla": "" }), knapp({ "data-urval-forening": "A" }),
      knapp({ "data-urval-forening": "B" }), grupp("A", ["x", "y"]), grupp("B", ["z"]),
    ], true),
    lista([sak("x"), sak("z"), sak("y|z")]),
    lista([sak("y")]),
    new Nod("a", { href: "pagar.html" }),
  ]);
  const fonster = new Nod("window");
  const plats = { search: sok, pathname: "/giffa/index.html" };
  const historik = { pushState(_s, _t, adress) { plats.search = adress.startsWith("?") ? adress : ""; } };
  vm.runInNewContext(SKRIPT, { document: dokument, window: fonster, location: plats, history: historik, URLSearchParams });
  return { dokument, fonster, plats };
}

const synligaOrter = (d) => d.querySelectorAll("li").filter((s) => !s.hidden).map((s) => s.getAttribute("data-ort"));
const tryckta = (d) => d.querySelectorAll("button").filter((k) => k.getAttribute("aria-pressed") === "true")
  .map((k) => k.getAttribute("data-urval-forening") || k.getAttribute("data-urval-ort") || "Alla");
const oppenGrupp = (d) => d.querySelectorAll("[data-urval-grupp]").filter((g) => !g.hidden)
  .map((g) => g.getAttribute("data-urval-grupp"));
const knappFor = (d, attribut, varde) => d.querySelectorAll("button").find((k) => k.getAttribute(attribut) === varde);

test("utan val syns allt och Alla är tryckt", () => {
  const { dokument } = sida("");
  assert.strictEqual(dokument.querySelector(".urval").hidden, false);
  assert.deepStrictEqual(synligaOrter(dokument), ["x", "z", "y|z", "y"]);
  assert.deepStrictEqual(tryckta(dokument), ["Alla"]);
  assert.deepStrictEqual(oppenGrupp(dokument), []);
});

test("en förening visar ärendena i sina orter och sina ortknappar", () => {
  const { dokument } = sida("?forening=A");
  assert.deepStrictEqual(synligaOrter(dokument), ["x", "y|z", "y"]);
  assert.deepStrictEqual(tryckta(dokument), ["A"]);
  assert.deepStrictEqual(oppenGrupp(dokument), ["A"]);
});

test("en ort visar bara sina ärenden, också när de har flera orter", () => {
  const { dokument } = sida("?ort=z");
  assert.deepStrictEqual(synligaOrter(dokument), ["z", "y|z"]);
  assert.deepStrictEqual(tryckta(dokument), ["B", "z"]);
});

test("en ort i en annan förening än ?forening= väljer ortens förening", () => {
  const { dokument } = sida("?forening=B&ort=x");
  assert.deepStrictEqual(synligaOrter(dokument), ["x"]);
  assert.deepStrictEqual(tryckta(dokument), ["A", "x"]);
  assert.deepStrictEqual(oppenGrupp(dokument), ["A"]);
});

test("en okänd förening eller ?ort=Alla visar allt", () => {
  for (const sok of ["?forening=Okänd", "?ort=Alla"]) {
    const { dokument } = sida(sok);
    assert.deepStrictEqual(synligaOrter(dokument), ["x", "z", "y|z", "y"], sok);
    assert.deepStrictEqual(tryckta(dokument), ["Alla"], sok);
  }
});

test("en lista som valet tömmer säger det och döljer tabellen", () => {
  const { dokument } = sida("?ort=x");
  const [forsta, andra] = dokument.querySelectorAll(".urvalslista");
  assert.strictEqual(forsta.querySelector(".inget-val").hidden, true);
  assert.strictEqual(andra.querySelector(".inget-val").hidden, false);
  assert.strictEqual(andra.querySelector(".tabell").hidden, true);
});

test("ett klick ändrar adressen och länkarna, Alla tar bort valet", () => {
  const { dokument, plats } = sida("");
  knappFor(dokument, "data-urval-forening", "B").click();
  assert.strictEqual(plats.search, "?forening=B");
  assert.strictEqual(dokument.querySelector("a").getAttribute("href"), "pagar.html?forening=B");
  assert.deepStrictEqual(synligaOrter(dokument), ["z", "y|z"]);
  knappFor(dokument, "data-alla", "").click();
  assert.strictEqual(plats.search, "");
  assert.strictEqual(dokument.querySelector("a").getAttribute("href"), "pagar.html");
  assert.deepStrictEqual(tryckta(dokument), ["Alla"]);
});

test("bakåt i webbläsaren läser valet ur adressen igen", () => {
  const { dokument, fonster, plats } = sida("?ort=x");
  plats.search = "?forening=B";
  fonster.click();
  assert.deepStrictEqual(tryckta(dokument), ["B"]);
  assert.deepStrictEqual(synligaOrter(dokument), ["z", "y|z"]);
});
