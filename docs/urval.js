// Krav: K4 och K21 i KRAV.md. Test: tests/test_bygg.py (att skriptet följer med).
// Utan skriptet står allt.
(function () {
  var SIDA = /^[\w./-]+\.html$/;

  function ortIAdressen() {
    return new URLSearchParams(location.search).get("ort");
  }

  function lankarMedOrt(ort) {
    Array.prototype.forEach.call(document.querySelectorAll("a[href]"), function (lank) {
      var sida = lank.getAttribute("href").split("?")[0];
      if (!SIDA.test(sida)) return;
      lank.setAttribute("href", ort ? sida + "?ort=" + encodeURIComponent(ort) : sida);
    });
  }

  function visa(knappar, ort) {
    Array.prototype.forEach.call(knappar, function (knapp) {
      knapp.setAttribute("aria-pressed", knapp.getAttribute("data-urval") === (ort || "Alla"));
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-ort]"), function (sak) {
      sak.hidden = ort !== null && sak.getAttribute("data-ort").split("|").indexOf(ort) < 0;
    });
    lankarMedOrt(ort);
  }

  function koppla(urval) {
    var knappar = urval.querySelectorAll("button");
    var orter = Array.prototype.map.call(knappar, function (k) { return k.getAttribute("data-urval"); });
    var giltig = function (ort) { return ort !== "Alla" && orter.indexOf(ort) >= 0 ? ort : null; };
    var vald = giltig(ortIAdressen());
    Array.prototype.forEach.call(knappar, function (knapp) {
      knapp.addEventListener("click", function () {
        var ort = giltig(knapp.getAttribute("data-urval"));
        if (ort === vald) return;
        vald = ort;
        history.pushState(null, "", ort ? "?ort=" + encodeURIComponent(ort) : location.pathname);
        visa(knappar, ort);
      });
    });
    window.addEventListener("popstate", function () {
      vald = giltig(ortIAdressen());
      visa(knappar, vald);
    });
    urval.hidden = false;
    visa(knappar, vald);
  }

  var urval = document.querySelector(".urval");
  if (urval) koppla(urval);
  else lankarMedOrt(ortIAdressen());
})();
