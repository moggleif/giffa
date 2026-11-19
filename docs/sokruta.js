// Krav: K28 i KRAV.md, beslut 0018. Test: tests/test_sokruta.js.
// Knappen Sök i sajtraden, som sajter.js just lagt till, fäller ut sökfältet under raden.
// Sökindexet sok.json hämtas första gången, och träffarna ritas medan man skriver: ärendena
// i urvalet i adressen och punkterna på KS-mötet, var för sig. Escape eller knappen fäller
// ihop fältet. På sidan Sök (data-sok-oppen) är fältet utfällt från början.
(function () {
  var MINST = 2;
  var skript = document.currentScript.getAttribute("src");
  var rot = skript.slice(0, skript.lastIndexOf("/") + 1);
  var index = null;
  var laddning = null;

  function element(tagg, attribut, text) {
    var e = document.createElement(tagg);
    Object.keys(attribut).forEach(function (namn) { e.setAttribute(namn, attribut[namn]); });
    if (text) e.textContent = text;
    return e;
  }

  function markerad(lank, text, ord) {
    Sokning.delar(text, ord).forEach(function (del) {
      lank.appendChild(del[1] ? element("mark", {}, del[0]) : document.createTextNode(del[0]));
    });
    return lank;
  }

  function rad(traff, adress, om, ord) {
    var li = element("li", {});
    li.appendChild(markerad(element("a", { href: adress }), traff.post.rubrik, ord));
    li.appendChild(element("small", {}, om.concat(traff.iTexten ? ["nämns i texten"] : []).join(" · ")));
    return li;
  }

  function arenderad(traff, ord) {
    var a = traff.post;
    var namn = Sokning.namnen(a, ord).map(function (n) { return "uppmärksammat som " + n; });
    return rad(traff, rot + a.adress + location.search, [a.orter.join(", "), a.status].concat(namn), ord);
  }

  function punktrad(traff, ord) {
    var p = traff.post;
    return rad(traff, rot + p.adress, ["Punkt " + p.nummer].concat(p.dnr ? ["Dnr " + p.dnr] : []), ord);
  }

  function grupp(resultat, rubrik, traffar, ritaRad) {
    if (!traffar.length) return;
    resultat.appendChild(element("h2", {}, rubrik + " (" + traffar.length + ")"));
    var ul = resultat.appendChild(element("ul", {}));
    traffar.forEach(function (t) { ul.appendChild(ritaRad(t)); });
  }

  function urvalet() {
    var fraga = new URLSearchParams(location.search);
    return Sokning.urvalet(index.foreningar, fraga.get("forening"), fraga.get("ort"));
  }

  function visa(panel, status, antal) {
    status.textContent = antal ? antal + (antal === 1 ? " träff" : " träffar") : "Inga träffar.";
    status.className = antal ? "dold" : "";
    panel.querySelector(".sokresultat").hidden = !antal;
  }

  function rita(panel, fraga) {
    var resultat = panel.querySelector(".sokresultat");
    var status = panel.querySelector("[role=status]");
    var ord = Sokning.orden(fraga);
    resultat.textContent = "";
    status.textContent = "";
    if (ord.join("").length < MINST) return;
    var urval = urvalet();
    var arenden = Sokning.traffar(Sokning.iUrvalet(index.arenden, urval), ord);
    var punkter = index.motet ? Sokning.traffar(index.motet.punkter, ord) : [];
    var rubrik = urval ? "Ärenden i " + urval.namn : "Ärenden";
    grupp(resultat, rubrik, arenden, function (t) { return arenderad(t, ord); });
    if (index.motet) grupp(resultat, index.motet.rubrik, punkter, function (t) { return punktrad(t, ord); });
    visa(panel, status, arenden.length + punkter.length);
  }

  function ladda() {
    laddning = laddning || fetch(rot + "sok.json").then(function (svar) {
      if (!svar.ok) throw new Error("sok.json: " + svar.status);
      return svar.json();
    }).then(function (laddat) { index = laddat; });
    return laddning;
  }

  function sok(panel, falt) {
    ladda().then(function () { rita(panel, falt.value); }, function () {
      laddning = null;
      panel.querySelector("[role=status]").textContent = "Sökningen gick inte att ladda.";
    });
  }

  function panelen() {
    var panel = element("div", { id: "sokpanel", "class": "sokpanel", role: "search" });
    panel.hidden = true;
    panel.appendChild(element("label", { "for": "sokfalt", "class": "dold" }, "Sök på Giffå"));
    var falt = panel.appendChild(element("input", {
      id: "sokfalt", type: "search", autocomplete: "off", placeholder: "Sök på Giffå"
    }));
    panel.appendChild(element("p", { role: "status" }));
    panel.appendChild(element("div", { "class": "sokresultat" }));
    falt.addEventListener("input", function () { sok(panel, falt); });
    return panel;
  }

  function vaxla(knapp, panel, oppen) {
    knapp.setAttribute("aria-expanded", String(oppen));
    panel.hidden = !oppen;
    if (oppen) sok(panel, panel.querySelector("input"));
  }

  var sajtrad = document.querySelector(".sajtrad").querySelector("div");
  var meny = document.querySelector(".sajtmeny");
  var knapp = element("button", {
    type: "button", "class": "sokknapp", "aria-expanded": "false", "aria-controls": "sokpanel"
  }, "Sök");
  var panel = panelen();
  sajtrad.insertBefore(knapp, sajtrad.querySelector(".temaknapp") || sajtrad.querySelector(".menyknapp"));
  meny.parentNode.insertBefore(panel, meny);
  knapp.addEventListener("click", function () {
    vaxla(knapp, panel, panel.hidden);
    if (!panel.hidden) panel.querySelector("input").focus();
  });
  // Escape stänger bara fältet; sajter.js ska inte också stänga menyn och flytta fokus dit.
  panel.addEventListener("keydown", function (h) {
    if (h.key !== "Escape") return;
    h.stopPropagation();
    vaxla(knapp, panel, false);
    knapp.focus();
  });
  if (document.querySelector("[data-sok-oppen]")) vaxla(knapp, panel, true);
})();
