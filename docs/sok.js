// Krav: K28 i KRAV.md. Test: tests/test_sok.js.
// Visar de ärenden där varje sökord finns i data-sok. Utan skript står hela listan.
(function () {
  function sokord(text) {
    return text.toLowerCase().split(/\s+/).filter(function (ord) { return ord; });
  }

  function passar(orden, text) {
    return orden.every(function (ord) { return text.indexOf(ord) >= 0; });
  }

  function filtrera(falt, poster, ingen) {
    var orden = sokord(falt.value);
    var traffar = 0;
    poster.forEach(function (post) {
      post.hidden = !passar(orden, post.getAttribute("data-sok"));
      if (!post.hidden) traffar += 1;
    });
    ingen.hidden = traffar > 0;
  }

  var falt = document.getElementById("sok");
  if (!falt) return;
  var poster = Array.prototype.slice.call(document.querySelectorAll("[data-sok]"));
  var ingen = document.querySelector(".ingen-traff");
  falt.addEventListener("input", function () { filtrera(falt, poster, ingen); });
  falt.parentNode.hidden = false;
  filtrera(falt, poster, ingen);
})();
