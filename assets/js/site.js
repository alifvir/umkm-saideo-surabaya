(function () {
  var tombol = document.querySelector("[data-nav-tombol]");
  var nav = document.querySelector("[data-nav]");
  if (!tombol || !nav) return;

  function setel(buka) {
    nav.setAttribute("data-terbuka", buka ? "true" : "false");
    tombol.setAttribute("aria-expanded", buka ? "true" : "false");
  }

  tombol.addEventListener("click", function () {
    setel(nav.getAttribute("data-terbuka") !== "true");
  });

  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) setel(false);
  });

  document.addEventListener("click", function (e) {
    if (!nav.contains(e.target) && !tombol.contains(e.target)) setel(false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav.getAttribute("data-terbuka") === "true") {
      setel(false);
      tombol.focus();
    }
  });
})();
