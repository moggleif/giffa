// Krav: K35 och K36 i KRAV.md, beslut 0013–0015. Kör docs/sajter.js och docs/tema.js mot
// en liten påhittad sida:
// node --test tests/*.js
"use strict";
const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const SKRIPT = fs.readFileSync(path.join(__dirname, "..", "docs", "sajter.js"), "utf8");
const TEMA = fs.readFileSync(path.join(__dirname, "..", "docs", "tema.js"), "utf8");

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
  setAttribute(namn, varde) {
    this.attribut[namn] = String(varde);
    if (namn === "class") String(varde).split(" ").forEach((k) => this.classList.add(k));
  }
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
  const document = Object.assign(kropp, { createElement: (tagg) => new El(tagg), documentElement: { dataset: {} } });
  vm.runInNewContext(SKRIPT, { document, location: { pathname: sokvag }, ...webblasare() });
  return { kropp, meny, hoppa, undermenyer: meny.querySelectorAll("details") };
}

// Det tema.js och temaknappen behöver av webbläsaren: stöd för light-dark(), läsarens
// inställning och lagringen.
function webblasare({ stod = true, morkInstallning = false, sparat = {} } = {}) {
  const CSS = { supports: () => stod };
  const localStorage = {
    getItem: (nyckel) => (nyckel in sparat ? sparat[nyckel] : null),
    setItem: (nyckel, varde) => { sparat[nyckel] = varde; },
  };
  return { window: { CSS }, CSS, localStorage, matchMedia: () => ({ matches: morkInstallning }) };
}

test("sajtraden står mellan hopplänken och menyn, med den här sajten markerad", () => {
  const { kropp, meny, hoppa } = sida("/giffa/pagar.html");
  const rad = kropp.barn[1];
  assert.deepStrictEqual([kropp.barn[0], kropp.barn[2]], [hoppa, meny]);
  assert.strictEqual(rad.getAttribute("aria-label"), "Sajterna");
  const lankar = rad.querySelectorAll("a");
  assert.deepStrictEqual(lankar.map((a) => a.textContent), ["Giffå", "Kungsbacka kommun", "Kungsbacka i siffror", "Region Halland"]);
  assert.deepStrictEqual(lankar.map((a) => a.getAttribute("href")), [
    "https://moggleif.github.io/giffa/",
    "https://moggleif.github.io/kungsbackakommun/",
    "https://moggleif.github.io/politik/",
    "https://moggleif.github.io/regionhalland/",
  ]);
  assert.deepStrictEqual(lankar.map((a) => a.getAttribute("aria-current")), ["true", null, null, null]);
});

test("på en annan sajt är den markerad i stället", () => {
  const { kropp } = sida("/politik/grundskolor.html");
  const markerade = kropp.barn[1].querySelectorAll("[aria-current]").map((a) => a.textContent);
  assert.deepStrictEqual(markerade, ["Kungsbacka i siffror"]);
});

test("knappen Meny står i sajtraden och fäller ut och ihop menyn", () => {
  const { kropp, meny } = sida("/giffa/");
  const knapp = kropp.barn[1].querySelector(".menyknapp");
  assert.strictEqual(knapp.textContent, "Meny");
  assert.ok(meny.classList.contains("har-knapp"));
  knapp.skicka("click");
  assert.strictEqual(knapp.getAttribute("aria-expanded"), "true");
  assert.ok(meny.classList.contains("oppen"));
  knapp.skicka("click");
  assert.strictEqual(knapp.getAttribute("aria-expanded"), "false");
  assert.ok(!meny.classList.contains("oppen"));
});

test("sajtens rad är märkt, och de andra sajterna står sist i menyn", () => {
  const { kropp, meny } = sida("/politik/");
  const rad = kropp.barn[1];
  assert.ok(rad.classList.contains("kand") && meny.classList.contains("kand"));
  const denna = rad.querySelectorAll("li").filter((li) => li.classList.contains("denna"));
  assert.deepStrictEqual(denna.map((li) => li.querySelector("a").textContent), ["Kungsbacka i siffror"]);
  const sist = meny.barn.at(-1);
  assert.ok(sist.classList.contains("andra-sajter"));
  assert.strictEqual(sist.querySelector("p").textContent, "Projektets andra sajter");
  assert.deepStrictEqual(sist.querySelectorAll("a").map((a) => a.textContent), ["Giffå", "Kungsbacka kommun", "Region Halland"]);
  assert.ok(sist.querySelectorAll("a").every((a) => a.getAttribute("aria-current") === null));
  assert.strictEqual(meny.querySelector("ul").barn.length, 3);
});

test("på en okänd adress behåller sajten sitt eget namn", () => {
  const { kropp, meny } = sida("/forhandsvisning/");
  assert.ok(!kropp.barn[1].classList.contains("kand"));
  assert.ok(!meny.classList.contains("kand"));
  assert.strictEqual(meny.querySelector(".andra-sajter"), null);
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
  const knapp = kropp.barn[1].querySelector(".menyknapp");
  knapp.click();
  kropp.skicka("keydown", { key: "Escape" });
  assert.ok(!meny.classList.contains("oppen"));
  assert.ok("fokus" in knapp.attribut);
});

test("en sajt utan undermenyer får sajtraden och knappen", () => {
  const { kropp, meny } = sida("/kungsbackakommun/kungsbacka.html", [lank(), lank()]);
  assert.strictEqual(kropp.barn[1].querySelector("[aria-current]").textContent, "Kungsbacka kommun");
  assert.ok(meny.classList.contains("har-knapp"));
  assert.strictEqual(kropp.barn[1].querySelector(".menyknapp").textContent, "Meny");
  kropp.skicka("keydown", { key: "Escape" });
});

function temasida(installningar) {
  const meny = new El("nav", { class: "sajtmeny" }, [new El("ul", {}, [lank()])]);
  const kropp = new El("body", {}, [meny]);
  const rot = { dataset: {} };
  const document = Object.assign(kropp, { createElement: (tagg) => new El(tagg), documentElement: rot });
  const miljo = { document, location: { pathname: "/giffa/" }, ...webblasare(installningar) };
  vm.runInNewContext(TEMA, miljo);
  vm.runInNewContext(SKRIPT, miljo);
  return { kropp, rot, knapp: kropp.querySelector(".temaknapp") };
}

test("temaknappen står i sajtraden före Meny och följer läsarens inställning", () => {
  const { kropp, rot, knapp } = temasida({ morkInstallning: true });
  const knappar = kropp.barn[0].querySelectorAll("button");
  assert.deepStrictEqual(knappar.map((k) => k.getAttribute("class")), ["temaknapp", "menyknapp"]);
  assert.strictEqual(knapp.getAttribute("aria-label"), "Mörkt tema");
  assert.strictEqual(knapp.getAttribute("aria-pressed"), "true");
  assert.strictEqual(rot.dataset.tema, "");
});

test("ett klick byter tema och sparar valet för alla sajterna", () => {
  const sparat = {};
  const { rot, knapp } = temasida({ sparat });
  assert.strictEqual(knapp.getAttribute("aria-pressed"), "false");
  knapp.click();
  assert.deepStrictEqual([rot.dataset.tema, knapp.getAttribute("aria-pressed")], ["morkt", "true"]);
  assert.deepStrictEqual(sparat, { "sajter-tema": "morkt" });
  knapp.click();
  assert.deepStrictEqual([rot.dataset.tema, knapp.getAttribute("aria-pressed")], ["ljust", "false"]);
  assert.deepStrictEqual(sparat, { "sajter-tema": "ljust" });
});

test("ett sparat val gäller före läsarens inställning", () => {
  const { rot, knapp } = temasida({ morkInstallning: true, sparat: { "sajter-tema": "ljust" } });
  assert.strictEqual(rot.dataset.tema, "ljust");
  assert.strictEqual(knapp.getAttribute("aria-pressed"), "false");
});

test("en webbläsare utan light-dark() får ingen temaknapp och inget tema", () => {
  const { rot, knapp } = temasida({ stod: false, sparat: { "sajter-tema": "morkt" } });
  assert.strictEqual(knapp, null);
  assert.strictEqual(rot.dataset.tema, undefined);
});
