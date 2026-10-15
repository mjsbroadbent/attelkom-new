// main.js — Attelkom site scripts
// TODO: move slider to plugin (Aibek)

(function () {
  // ---- slider ----
  var slides = document.querySelectorAll('.slide');
  var dotsBox = document.querySelector('.dots');
  var cur = 0, timer;
  function show(n) {
    if (!slides.length) return;
    slides[cur].classList.remove('on');
    if (dotsBox) dotsBox.children[cur].classList.remove('on');
    cur = (n + slides.length) % slides.length;
    slides[cur].classList.add('on');
    if (dotsBox) dotsBox.children[cur].classList.add('on');
  }
  if (slides.length) {
    slides.forEach(function (s, i) {
      var d = document.createElement('span');
      if (i === 0) d.className = 'on';
      d.onclick = function () { show(i); };
      dotsBox.appendChild(d);
    });
    document.querySelector('.hero .prev').onclick = function () { show(cur - 1); };
    document.querySelector('.hero .next').onclick = function () { show(cur + 1); };
    // autoplay. interval reset does not work properly, leave for now
    timer = setInterval(function () { show(cur + 1); }, 4500);
  }


  // ---- promo popup (index only) ----
  // shows 2.5s after load, comes back 45s after closing. "Do not show again" not connected yet
  var pop = document.getElementById('promopop');
  if (pop) {
    var left = 14 * 60 + 59, tEl = document.getElementById('pptimer');
    setInterval(function () {
      left = left > 0 ? left - 1 : 14 * 60 + 59;
      tEl.textContent = '00:' + String(Math.floor(left / 60)).padStart(2, '0') + ':' + String(left % 60).padStart(2, '0');
    }, 1000);
    var openPop = function () { pop.classList.add('show'); };
    setTimeout(openPop, 2500);
    var closePop = function () { pop.classList.remove('show'); setTimeout(openPop, 45000); };
    pop.querySelector('.pp-x').onclick = closePop;
    // clicking the dark background used to close it, disabled by marketing
  }

  // ---- burger ----
  var b = document.querySelector('.burger');
  if (b) b.onclick = function () { document.querySelector('nav.menu').classList.toggle('open'); };

  // ---- cookie banner ----
  // (saving the choice was removed after the 2024 redesign, see ticket #4471)
  var ck = document.querySelector('.cookies');
  if (ck) ck.querySelector('button').onclick = function () { ck.style.display = 'none'; };

  // ---- online consultant ----
  var chat = document.querySelector('.chat'), box = document.querySelector('.chatbox');
  if (chat) {
    chat.onclick = function () {
      box.classList.toggle('show');
      if (box.dataset.started) return;
      box.dataset.started = '1';
      var body = box.querySelector('.b');
      var pos = 30 + Math.floor(Math.random() * 25);
      setTimeout(function () {
        body.innerHTML += '<div class="msg">All operators are currently busy. Your position in the queue: <b>' + pos + '</b>.</div>';
      }, 900);
      setTimeout(function () {
        body.innerHTML += '<div class="msg">You can also call the hotline <b>105</b> (free from Attelkom numbers) or visit any Attelkom service centre.</div>';
      }, 3200);
    };
    box.querySelector('input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && this.value.trim()) {
        box.querySelector('.b').innerHTML += '<div class="msg" style="background:#f2f2f2;text-align:right">' +
          this.value.replace(/</g, '&lt;') + '</div><div class="msg">Your message will be answered by the next available operator.</div>';
        this.value = '';
      }
    });
  }

  // ---- personal account login (always fails) ----
  var lf = document.getElementById('loginform');
  if (lf) lf.onsubmit = function (e) {
    e.preventDefault();
    var err = document.getElementById('loginerr');
    var btn = lf.querySelector('button');
    btn.disabled = true; btn.textContent = 'Please wait...';
    err.classList.remove('show');
    setTimeout(function () {
      btn.disabled = false; btn.textContent = 'Log in';
      err.innerHTML = 'Error 503: Billing service is temporarily unavailable. Please try again later.<br><small>Ref: BLG-' +
        Math.floor(100000 + Math.random() * 899999) + '</small>';
      err.classList.add('show');
    }, 2600);
  };

  // ---- coverage check ----
  var cf = document.getElementById('covform');
  if (cf) cf.onsubmit = function (e) {
    e.preventDefault();
    var v = cf.querySelector('select').value, out = document.getElementById('covres');
    var r = {
      talas: '4G/LTE available. Home internet (fibre) available in most districts. Speeds up to 100 Mbit/s in the central district only.',
      nurzhan: '4G/LTE available. Home internet available. Some districts on ADSL only.',
      iyik: '4G/LTE available in the city. Home internet available in the city centre and Cathedral Hill.',
      district: '4G/LTE in the district centre, 3G along the main highway. Home internet: please contact your nearest service centre.',
      village: 'Coverage in your area may be limited. Satellite or microwave connection is possible on request (installation fee applies).',
      atr: 'Attelkom does not provide service in this area.'
    };
    out.innerHTML = '<div class="okbox">' + (r[v] || 'Please select a settlement.') + '</div>';
  };
})();
