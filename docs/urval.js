// Krav: K4 och K21 i KRAV.md. Test: tests/test_bygg.py (att skriptet följer med).
// Visar bara raderna och korten för den ort som valts med en knapp. Valet
// står i adressen (?ort=Åsa), så att länken går att dela och bakåtknappen
// fungerar, och menyns länkar tar med det till nästa sida.
// Utan skriptet står allt.
(function () {
  var urval = document.querySelector(".urval");
  if (!urval) return;
  var knappar = urval.querySelectorAll("button");
  var orter = Array.prototype.map.call(knappar, function (k) {
    return k.getAttribute("data-urval");
  });

  function ortIAdressen() {
    var ort = new URLSearchParams(location.search).get("ort");
    return orter.indexOf(ort) > 0 ? ort : "Alla";
  }

  function fraga(ort) {
    return ort === "Alla" ? location.pathname : "?ort=" + encodeURIComponent(ort);
  }

  function visa(ort) {
    Array.prototype.forEach.call(knappar, function (knapp) {
      knapp.setAttribute("aria-pressed", knapp.getAttribute("data-urval") === ort);
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-ort]"), function (sak) {
      sak.hidden = ort !== "Alla" && sak.getAttribute("data-ort").split("|").indexOf(ort) < 0;
    });
    Array.prototype.forEach.call(document.querySelectorAll("nav a"), function (lank) {
      var sida = lank.getAttribute("href").split("?")[0];
      lank.setAttribute("href", ort === "Alla" ? sida : sida + fraga(ort));
    });
  }

  Array.prototype.forEach.call(knappar, function (knapp) {
    knapp.addEventListener("click", function () {
      var ort = knapp.getAttribute("data-urval");
      history.pushState(null, "", fraga(ort));
      visa(ort);
    });
  });
  window.addEventListener("popstate", function () {
    visa(ortIAdressen());
  });
  urval.hidden = false;
  visa(ortIAdressen());
})();
