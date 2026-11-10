// Krav: K4 i KRAV.md. Test: tests/test_bygg.py (att skriptet följer med).
// Visar bara raderna och korten för den ort som valts med en knapp.
// Utan skriptet står allt.
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

  Array.prototype.forEach.call(knappar, function (knapp) {
    knapp.addEventListener("click", function () {
      valj(knapp.getAttribute("data-urval"));
    });
  });
  urval.hidden = false;
  valj("Alla");
})();
