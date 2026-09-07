// data-vault catalog filtering — vanilla JS
(function () {
  var chips = document.querySelectorAll('.chip');
  var cards = document.querySelectorAll('.card[data-niche]');
  var count = document.getElementById('count');
  if (!chips.length) return;

  function apply(filter) {
    var shown = 0;
    cards.forEach(function (c) {
      var hit = filter === 'all' || c.dataset.niche === filter;
      c.classList.toggle('hidden', !hit);
      if (hit) shown++;
    });
    if (count) count.textContent = shown;
    chips.forEach(function (ch) {
      ch.setAttribute('aria-pressed', ch.dataset.filter === filter ? 'true' : 'false');
    });
  }

  chips.forEach(function (ch) {
    ch.addEventListener('click', function () { apply(ch.dataset.filter); });
  });

  // deep link: index.html#real-estate
  if (location.hash) {
    var f = location.hash.slice(1);
    for (var i = 0; i < chips.length; i++) {
      if (chips[i].dataset.filter === f) { apply(f); break; }
    }
  }
})();
