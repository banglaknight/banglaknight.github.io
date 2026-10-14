// BanglaKnight site: mobile menu, home-page date card and countdown, Data-page example.

(function () {
  // Mobile menu.
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Dates: a date counts as passed at the end of that day, Anywhere on Earth (UTC-12).
  function endOfDayAoE(iso) {
    var p = iso.split("-").map(Number);
    return Date.UTC(p[0], p[1] - 1, p[2], 23, 59, 59) + 12 * 3600 * 1000;
  }
  var now = Date.now();

  function markDates(selector, onNext) {
    var rows = document.querySelectorAll(selector);
    var nextIso = null;
    rows.forEach(function (row) {
      var iso = row.getAttribute("data-date");
      var passed = endOfDayAoE(iso) < now;
      if (passed) {
        row.classList.add("is-past");
      } else if (nextIso === null || iso === nextIso) {
        nextIso = iso;
        row.classList.add("is-next");
        if (onNext) onNext(row, iso);
      }
    });
    return nextIso;
  }

  // Home page card.
  var nextTitles = [];
  var cardNext = markDates(".dc-list li[data-date]", function (li) {
    nextTitles.push(li.querySelector(".dc-title").textContent);
  });
  var countdown = document.querySelector(".dc-countdown");
  if (countdown && cardNext) {
    // Count to the start of that day (AoE).
    var days = Math.ceil((endOfDayAoE(cardNext) - 86399000 - now) / 86400000);
    // Lowercase the first letter ("Training..." -> "training...") but keep names such as CodaBench.
    var what = nextTitles.map(function (t) {
      return /^[A-Z][a-z]+[A-Z]/.test(t) ? t : t.charAt(0).toLowerCase() + t.slice(1);
    }).join(" and ");
    countdown.innerHTML = days <= 0
      ? "<strong>Today</strong> " + what
      : "<strong>" + days + " days</strong> until " + what;
    countdown.hidden = false;
  }

  // Data page: the same request in three written forms.
  var bubble = document.getElementById("demo-text");
  if (bubble) {
    var forms = [
      { text: "আজ ঢাকায় আবহাওয়া কেমন থাকবে?", lang: "bn" },
      { text: "Aaj Dhakay abhawa kemon thakbe?", lang: "en" },
      { text: "আজ Dhaka-তে weather কেমন থাকবে?", lang: "bn" }
    ];
    var tabs = document.querySelectorAll(".demo-tabs .tab");
    var current = 0;
    var timer = null;
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var show = function (i) {
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
    };

    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        clearInterval(timer);
        show(Number(t.dataset.form));
      });
    });
    if (!reduceMotion) {
      timer = setInterval(function () { show((current + 1) % forms.length); }, 3200);
    }
  }
})();
