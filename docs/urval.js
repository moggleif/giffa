// Krav: K4, K21 och K22 i KRAV.md. Test: tests/test_urval.js, och tests/test_bygg.py (att skriptet följer med).
// Valet är en förening, en ort eller båda; inget val visar allt. Föreningen
// begränsar vilka ortknappar som syns, orten vilka ärenden. Utan skriptet står allt.
(function () {
  var SIDA = /^[\w./-]+\.html$/;
  var INGET = { forening: null, ort: null };

  function alla(valjare, rot) {
    return Array.prototype.slice.call((rot || document).querySelectorAll(valjare));
  }

  function fraga(val) {
    var delar = [];
    if (val.forening) delar.push("forening=" + encodeURIComponent(val.forening));
    if (val.ort) delar.push("ort=" + encodeURIComponent(val.ort));
    return delar.length ? "?" + delar.join("&") : "";
  }

  function lankar(val) {
    alla("a[href]").forEach(function (lank) {
      var sida = lank.getAttribute("href").split("?")[0];
      if (SIDA.test(sida)) lank.setAttribute("href", sida + fraga(val));
    });
  }

  function adressen() {
    var p = new URLSearchParams(location.search);
    return { forening: p.get("forening"), ort: p.get("ort") };
  }

  function orterI(grupp) {
    return alla("[data-urval-ort]", grupp).map(function (k) { return k.getAttribute("data-urval-ort"); });
  }

  function gruppen(grupper, forening) {
    return grupper.filter(function (g) { return g.getAttribute("data-urval-grupp") === forening; })[0];
  }

  function giltigt(grupper, val) {
    var grupp = gruppen(grupper, val.forening);
    var ortGrupper = grupp ? [grupp] : grupper;
    var ortFinns = ortGrupper.some(function (g) { return orterI(g).indexOf(val.ort) >= 0; });
    return { forening: grupp ? val.forening : null, ort: ortFinns ? val.ort : null };
  }

  function synliga(grupper, val) {
    if (val.ort) return [val.ort];
    var grupp = gruppen(grupper, val.forening);
    return grupp ? orterI(grupp) : null;
  }

  function tryckt(knapp, val) {
    if (knapp.hasAttribute("data-alla")) return !val.forening && !val.ort;
    var forening = knapp.getAttribute("data-urval-forening");
    if (forening !== null) return forening === val.forening;
    return knapp.getAttribute("data-urval-ort") === val.ort;
  }

  function visaSaker(orter) {
    alla("[data-ort]").forEach(function (sak) {
      sak.hidden = orter !== null && !sak.getAttribute("data-ort").split("|").some(function (o) {
        return orter.indexOf(o) >= 0;
      });
    });
  }

  function visaTomt() {
    alla(".urvalslista").forEach(function (lista) {
      var tomt = !alla("[data-ort]", lista).some(function (sak) { return !sak.hidden; });
      lista.querySelector(".inget-val").hidden = !tomt;
      alla(".tabell", lista).forEach(function (t) { t.hidden = tomt; });
    });
  }

  function visa(urval, grupper, val) {
    alla("button", urval).forEach(function (k) { k.setAttribute("aria-pressed", tryckt(k, val)); });
    grupper.forEach(function (g) {
      g.hidden = val.forening !== null && g.getAttribute("data-urval-grupp") !== val.forening;
    });
    visaSaker(synliga(grupper, val));
    visaTomt();
    lankar(val);
  }

  // En tryckt knapp som trycks igen släpper sitt val; det andra valet står kvar.
  function valet(knapp, vald) {
    if (knapp.hasAttribute("data-alla")) return INGET;
    var forening = knapp.getAttribute("data-urval-forening");
    if (forening !== null) {
      return { forening: forening === vald.forening ? null : forening, ort: vald.ort };
    }
    var ort = knapp.getAttribute("data-urval-ort");
    return { forening: vald.forening, ort: ort === vald.ort ? null : ort };
  }

  function koppla(urval) {
    var grupper = alla("[data-urval-grupp]", urval);
    var vald = giltigt(grupper, adressen());
    alla("button", urval).forEach(function (knapp) {
      knapp.addEventListener("click", function () {
        var val = giltigt(grupper, valet(knapp, vald));
        if (fraga(val) === fraga(vald)) return;
        vald = val;
        history.pushState(null, "", fraga(val) || location.pathname);
        visa(urval, grupper, val);
      });
    });
    window.addEventListener("popstate", function () {
      vald = giltigt(grupper, adressen());
      visa(urval, grupper, vald);
    });
    urval.hidden = false;
    visa(urval, grupper, vald);
  }

  var urval = document.querySelector(".urval");
  if (urval) koppla(urval);
  else lankar(adressen());
})();
