// Krav: K4 i KRAV.md. Test: tests/test_bygg.py (att skriptet följer med).
// Visar bara raderna och korten för den ort som valts med en knapp, och
// öppnar kortets historik när ett ärende väljs i tabellen.
// Utan skriptet står allt och historiken är hopfälld.
(function () {
  var urval = document.querySelector(".urval");
  if (!urval) return;
  var knappar = urval.querySelectorAll("button");

  function valj(ort) {
    Array.prototype.forEach.call(knappar, function (knapp) {
      knapp.setAttribute("aria-pressed", knapp.getAttribute("data-urval") === ort);
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-ort]"), function (sak) {
      sak.hidden = ort !== "Alla" && sak.getAttribute("data-ort").split("|").indexOf(ort) < 0;
    });
  }

  function oppna() {
    var kort = document.getElementById(location.hash.slice(1));
    if (kort && kort.tagName === "ARTICLE") kort.querySelector("details").open = true;
  }

  Array.prototype.forEach.call(knappar, function (knapp) {
    knapp.addEventListener("click", function () {
      valj(knapp.getAttribute("data-urval"));
    });
  });
  window.addEventListener("hashchange", oppna);
  urval.hidden = false;
  valj("Alla");
  oppna();
})();
