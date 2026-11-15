// Krav: K35 i KRAV.md, beslut 0013. Kör docs/sajter.js mot en liten påhittad sida:
// node --test tests/*.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const SKRIPT = fs.readFileSync(path.join(__dirname, "..", "docs", "sajter.js"), "utf8");

// Ett element med just det sajter.js använder.
class El {
  constructor(tagg, attribut = {}, barn = []) {
    const klasser = new Set((attribut.class || "").split(" ").filter(Boolean));
    Object.assign(this, { tagg, attribut, barn: [], lyssnare: {}, open: false, textContent: "" });
    this.classList = {
      add: (k) => klasser.add(k),
      toggle: (k, pa) => (pa ? klasser.add(k) : klasser.delete(k)),
      contains: (k) => klasser.has(k),
    };
    barn.forEach((b) => this.appendChild(b));
  }
  setAttribute(namn, varde) { this.attribut[namn] = String(varde); }
  getAttribute(namn) { return namn in this.attribut ? this.attribut[namn] : null; }
  appendChild(b) { b.parentNode = this; this.barn.push(b); return b; }
  insertBefore(b, fore) { b.parentNode = this; this.barn.splice(this.barn.indexOf(fore), 0, b); return b; }
  click() { this.skicka("click"); }
  focus() { this.attribut.fokus = ""; }
  addEventListener(typ, fn) { (this.lyssnare[typ] = this.lyssnare[typ] || []).push(fn); }
  skicka(typ, handelse = {}) { (this.lyssnare[typ] || []).forEach((fn) => fn(handelse)); }
  efterkommande() { return this.barn.flatMap((b) => [b, ...b.efterkommande()]); }
  contains(nod) { return nod === this || this.efterkommande().includes(nod); }
  passar(valjare) {
    if (valjare.startsWith(".")) return this.classList.contains(valjare.slice(1));
    if (valjare.startsWith("[")) return valjare.slice(1, -1) in this.attribut;
    return this.tagg === valjare;
  }
  querySelectorAll(valjare) { return this.efterkommande().filter((e) => e.passar(valjare)); }
  querySelector(valjare) { return this.querySelectorAll(valjare)[0] || null; }
}

const lank = (attribut = {}) => new El("li", {}, [new El("a", attribut)]);
const undermeny = (lankar) => new El("li", {}, [new El("details", {}, [new El("summary"), new El("ul", {}, lankar)])]);

function sida(sokvag, poster = [lank(), undermeny([lank({ "aria-current": "page" }), lank()]), undermeny([lank()])]) {
  const meny = new El("nav", { class: "sajtmeny" }, [new El("a", { class: "sajtnamn" }), new El("ul", {}, poster)]);
  const hoppa = new El("a", { class: "hoppa" });
  const kropp = new El("body", {}, [hoppa, meny, new El("main")]);
  const document = Object.assign(kropp, { createElement: (tagg) => new El(tagg) });
  vm.runInNewContext(SKRIPT, { document, location: { pathname: sokvag } });
  return { kropp, meny, hoppa, undermenyer: meny.querySelectorAll("details") };
}

test("sajtraden står mellan hopplänken och menyn, med den här sajten markerad", () => {
  const { kropp, meny, hoppa } = sida("/giffa/pagar.html");
  const rad = kropp.barn[1];
  assert.deepStrictEqual([kropp.barn[0], kropp.barn[2]], [hoppa, meny]);
  assert.strictEqual(rad.getAttribute("aria-label"), "Sajterna");
  const lankar = rad.querySelectorAll("a");
  assert.deepStrictEqual(lankar.map((a) => a.textContent), ["Giffå", "Kungsbacka kommun", "Kungsbacka i siffror"]);
  assert.deepStrictEqual(lankar.map((a) => a.getAttribute("href")), [
    "https://moggleif.github.io/giffa/",
    "https://moggleif.github.io/kommunhandlingar/",
    "https://moggleif.github.io/politik/",
  ]);
  assert.deepStrictEqual(lankar.map((a) => a.getAttribute("aria-current")), ["true", null, null]);
});

test("på en annan sajt är den markerad i stället", () => {
  const { kropp } = sida("/politik/grundskolor.html");
  const markerade = kropp.barn[1].querySelectorAll("[aria-current]").map((a) => a.textContent);
  assert.deepStrictEqual(markerade, ["Kungsbacka i siffror"]);
});

test("knappen Meny fäller ut och ihop menyn", () => {
  const { meny } = sida("/giffa/");
  const knapp = meny.querySelector("button");
  assert.strictEqual(knapp.textContent, "Meny");
  assert.ok(meny.classList.contains("har-knapp"));
  knapp.skicka("click");
  assert.strictEqual(knapp.getAttribute("aria-expanded"), "true");
  assert.ok(meny.classList.contains("oppen"));
  knapp.skicka("click");
  assert.strictEqual(knapp.getAttribute("aria-expanded"), "false");
  assert.ok(!meny.classList.contains("oppen"));
});

test("undermenyn med den aktuella sidan märks", () => {
  const { undermenyer } = sida("/giffa/");
  assert.deepStrictEqual(undermenyer.map((d) => d.classList.contains("aktuell")), [true, false]);
});

test("bara en undermeny öppen åt gången, och Escape eller ett klick utanför stänger", () => {
  const { kropp, meny, undermenyer: [forsta, andra] } = sida("/giffa/");
  forsta.open = true;
  forsta.skicka("toggle");
  andra.open = true;
  andra.skicka("toggle");
  assert.deepStrictEqual([forsta.open, andra.open], [false, true]);
  kropp.skicka("click", { target: meny.querySelector("summary") });
  assert.strictEqual(andra.open, true);
  kropp.skicka("click", { target: kropp.querySelector("main") });
  assert.strictEqual(andra.open, false);
  andra.open = true;
  kropp.skicka("keydown", { key: "Enter" });
  assert.strictEqual(andra.open, true);
  kropp.skicka("keydown", { key: "Escape" });
  assert.strictEqual(andra.open, false);
  assert.ok("fokus" in andra.querySelector("summary").attribut);
  forsta.open = true;
  meny.skicka("focusout", { relatedTarget: kropp.querySelector("main") });
  assert.strictEqual(forsta.open, false);
});

test("Escape fäller ihop den utfällda menyn när ingen undermeny är öppen", () => {
  const { kropp, meny } = sida("/giffa/");
  const knapp = meny.querySelector("button");
  knapp.click();
  kropp.skicka("keydown", { key: "Escape" });
  assert.ok(!meny.classList.contains("oppen"));
  assert.ok("fokus" in knapp.attribut);
});

test("en sajt utan undermenyer får sajtraden och knappen", () => {
  const { kropp, meny } = sida("/kommunhandlingar/kungsbacka.html", [lank(), lank()]);
  assert.strictEqual(kropp.barn[1].querySelector("[aria-current]").textContent, "Kungsbacka kommun");
  assert.strictEqual(meny.querySelector("button").textContent, "Meny");
  kropp.skicka("keydown", { key: "Escape" });
});
