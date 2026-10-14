// BanglaKnight site: demo tabs, mobile menu, active nav link.

(function () {
  // Demo: the same request in three written forms.
  var forms = [
    { text: "আজ ঢাকায় আবহাওয়া কেমন থাকবে?", lang: "bn" },
    { text: "Aaj Dhakay abhawa kemon thakbe?", lang: "en" },
    { text: "আজ Dhaka-তে weather কেমন থাকবে?", lang: "bn" }
  ];
  var tabs = document.querySelectorAll(".demo-tabs .tab");
  var bubble = document.getElementById("demo-text");
  var current = 0;
  var timer = null;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function show(i) {
    current = i;
    tabs.forEach(function (t, j) {
      t.classList.toggle("active", j === i);
      t.setAttribute("aria-selected", j === i ? "true" : "false");
    });
    bubble.classList.add("fade");
    setTimeout(function () {
      bubble.textContent = forms[i].text;
      bubble.lang = forms[i].lang;
      bubble.classList.remove("fade");
    }, reduceMotion ? 0 : 200);
  }

  function startRotation() {
    if (reduceMotion) return;
    timer = setInterval(function () { show((current + 1) % forms.length); }, 3200);
  }

  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      clearInterval(timer);
      show(Number(t.dataset.form));
    });
  });
  startRotation();

  // Mobile menu.
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  toggle.addEventListener("click", function () {
    var open = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  links.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      links.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });

  // Mark the nav link of the section in view.
  var navLinks = links.querySelectorAll('a[href^="#"]');
  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) {
          a.classList.toggle("active", a.getAttribute("href") === "#" + entry.target.id);
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    document.querySelectorAll("main section[id]").forEach(function (s) { observer.observe(s); });
  }
})();
