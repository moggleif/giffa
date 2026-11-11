// Krav: K4, K21 och K22 i KRAV.md. Test: tests/test_urval.js, och tests/test_bygg.py (att skriptet följer med).
// Valet är en förening, en ort eller båda; inget val visar allt. Föreningen
// begränsar vilka ortknappar som syns (data-urval-i), orten vilka ärenden. Utan skriptet står allt.
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

  function iForeningen(knapp, forening) {
    return forening === null || knapp.getAttribute("data-urval-i") === forening;
  }

  function orterI(ortknappar, forening) {
    return ortknappar.filter(function (k) { return iForeningen(k, forening); })
      .map(function (k) { return k.getAttribute("data-urval-ort"); });
  }

  function giltigt(ortknappar, val) {
    var finns = ortknappar.some(function (k) { return k.getAttribute("data-urval-i") === val.forening; });
    var forening = finns ? val.forening : null;
    var ort = orterI(ortknappar, forening).indexOf(val.ort) >= 0 ? val.ort : null;
    return { forening: forening, ort: ort };
  }

  function synliga(ortknappar, val) {
    if (val.ort) return [val.ort];
    return val.forening ? orterI(ortknappar, val.forening) : null;
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

  function visa(urval, ortknappar, val) {
    alla("button", urval).forEach(function (k) { k.setAttribute("aria-pressed", tryckt(k, val)); });
    ortknappar.forEach(function (k) { k.hidden = !iForeningen(k, val.forening); });
    visaSaker(synliga(ortknappar, val));
    visaTomt();
    lankar(val);
  }

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
    var ortknappar = alla("[data-urval-ort]", urval);
    var vald = giltigt(ortknappar, adressen());
    alla("button", urval).forEach(function (knapp) {
      knapp.addEventListener("click", function () {
        var val = giltigt(ortknappar, valet(knapp, vald));
        if (fraga(val) === fraga(vald)) return;
        vald = val;
        history.pushState(null, "", fraga(val) || location.pathname);
        visa(urval, ortknappar, val);
      });
    });
    window.addEventListener("popstate", function () {
      vald = giltigt(ortknappar, adressen());
      visa(urval, ortknappar, vald);
    });
    urval.hidden = false;
    visa(urval, ortknappar, vald);
  }

  var urval = document.querySelector(".urval");
  if (urval) koppla(urval);
  else lankar(adressen());
})();
