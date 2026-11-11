// Krav: K4, K21 och K22 i KRAV.md. Test: tests/test_bygg.py (att skriptet följer med).
// Valet är ingenting (allt syns), en förening eller en ort. Utan skriptet står allt.
(function () {
  var SIDA = /^[\w./-]+\.html$/;
  var INGET = { forening: null, ort: null };

  function alla(valjare, rot) {
    return Array.prototype.slice.call((rot || document).querySelectorAll(valjare));
  }

  function fraga(val) {
    if (val.ort) return "?ort=" + encodeURIComponent(val.ort);
    return val.forening ? "?forening=" + encodeURIComponent(val.forening) : "";
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

  function giltigt(grupper, val) {
    var medOrt = grupper.filter(function (g) { return orterI(g).indexOf(val.ort) >= 0; })[0];
    if (medOrt) return { forening: medOrt.getAttribute("data-urval-grupp"), ort: val.ort };
    var finns = grupper.some(function (g) { return g.getAttribute("data-urval-grupp") === val.forening; });
    return finns ? { forening: val.forening, ort: null } : INGET;
  }

  function synliga(grupper, val) {
    if (val.ort) return [val.ort];
    var grupp = grupper.filter(function (g) { return g.getAttribute("data-urval-grupp") === val.forening; })[0];
    return grupp ? orterI(grupp) : null;
  }

  function visa(urval, grupper, val) {
    alla("button", urval).forEach(function (k) {
      var namn = k.getAttribute("data-urval-forening");
      var pa = k.hasAttribute("data-alla") ? !val.forening
        : namn !== null ? namn === val.forening : k.getAttribute("data-urval-ort") === val.ort;
      k.setAttribute("aria-pressed", pa);
    });
    grupper.forEach(function (g) { g.hidden = g.getAttribute("data-urval-grupp") !== val.forening; });
    var orter = synliga(grupper, val);
    alla("[data-ort]").forEach(function (sak) {
      sak.hidden = orter !== null && !sak.getAttribute("data-ort").split("|").some(function (o) {
        return orter.indexOf(o) >= 0;
      });
    });
    alla(".inget-val").forEach(function (p) {
      var lista = p.previousElementSibling;
      var tabell = lista.previousElementSibling;
      p.hidden = alla("[data-ort]", lista).some(function (s) { return !s.hidden; });
      if (tabell && tabell.className === "tabell") tabell.hidden = !p.hidden;
    });
    lankar(val);
  }

  function valet(knapp) {
    if (knapp.hasAttribute("data-urval-forening")) {
      return { forening: knapp.getAttribute("data-urval-forening"), ort: null };
    }
    return { forening: null, ort: knapp.getAttribute("data-urval-ort") };
  }

  function koppla(urval) {
    var grupper = alla("[data-urval-grupp]", urval);
    var vald = giltigt(grupper, adressen());
    alla("button", urval).forEach(function (knapp) {
      knapp.addEventListener("click", function () {
        var val = knapp.hasAttribute("data-alla") ? INGET : giltigt(grupper, valet(knapp));
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
