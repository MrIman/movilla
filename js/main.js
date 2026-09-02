/* ==========================================================================
   MOVILLA — main.js (GSAP 3.14 + ScrollTrigger)
   Gramatyka ruchu: wszystko porusza się wzdłuż osi czasu (X).
   Tryb statyczny: prefers-reduced-motion albo ?static w adresie.
   ========================================================================== */
(() => {
  gsap.registerPlugin(ScrollTrigger);
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const STATIC = matchMedia('(prefers-reduced-motion: reduce)').matches || new URLSearchParams(location.search).has('static');
  const isTouch = matchMedia('(hover: none), (pointer: coarse)').matches;
  const body = document.body, html = document.documentElement;
  if (STATIC) html.classList.add('is-static');
  if (new URLSearchParams(location.search).has('capture')) html.classList.add('is-capture');
  gsap.defaults({ ease: 'expo.out', duration: 1 });
  const d = (v) => (STATIC ? 0 : v);

  /* ---------- linijka dni: kursor = postęp strony ---------- */
  const ruler = $('.ruler--top');
  if (ruler) {
    const cursor = $('.ruler__cursor', ruler), readout = $('[data-day]', ruler), scale = $('.ruler__scale', ruler);
    const max = parseFloat(ruler.dataset.max) || 60;
    const setDay = (p) => {
      const day = Math.round(p * max);
      readout.textContent = day;
      cursor.style.left = `calc(var(--gutter) + ${p * 100}% - ${p} * 2 * var(--gutter))`;
      cursor.classList.toggle('is-right', p > 0.82);
    };
    setDay(0);
    ScrollTrigger.create({ start: 0, end: () => ScrollTrigger.maxScroll(window), onUpdate: (s) => setDay(s.progress) });
    void scale;
  }

  /* ---------- pasek górny: aktywny link ---------- */
  const navLinks = $$('.topbar__nav a');
  $$('main section[id]').forEach((sec) => {
    const link = navLinks.find((a) => a.getAttribute('href').endsWith('#' + sec.id));
    if (!link) return;
    ScrollTrigger.create({ trigger: sec, start: 'top 45%', end: 'bottom 45%', onToggle: (s) => link.classList.toggle('is-active', s.isActive) });
  });

  /* ---------- menu mobilne ---------- */
  const menu = $('.menu'), burger = $('.topbar__burger');
  const toggleMenu = (open) => {
    const isOpen = open ?? !body.classList.contains('menu-open');
    body.classList.toggle('menu-open', isOpen);
    burger.setAttribute('aria-expanded', String(isOpen));
    menu.setAttribute('aria-hidden', String(!isOpen));
    if (isOpen) gsap.timeline().set(menu, { visibility: 'visible' }).to(menu, { x: 0, duration: d(0.7) })
      .from($$('.menu__links a'), { x: 40, opacity: 0, stagger: 0.03, duration: d(0.6) }, '-=0.5');
    else gsap.to(menu, { x: '102%', duration: d(0.5), ease: 'power3.in', onComplete: () => gsap.set(menu, { visibility: 'hidden' }) });
  };
  burger?.addEventListener('click', () => toggleMenu());
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && body.classList.contains('menu-open')) toggleMenu(false); });

  /* ---------- kotwice i przejścia między stronami ---------- */
  const veil = $('.veil');
  window.addEventListener('pageshow', (e) => { if (e.persisted && veil) gsap.set(veil, { scaleX: 0 }); });
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    const href = a.getAttribute('href');
    const hashIdx = href.indexOf('#');
    const samePage = hashIdx === 0 || (hashIdx > 0 && href.slice(0, hashIdx).split('/').pop() === location.pathname.split('/').pop());
    if (samePage) {
      const target = $(href.slice(hashIdx));
      if (target) {
        e.preventDefault();
        if (body.classList.contains('menu-open')) toggleMenu(false);
        target.scrollIntoView({ behavior: STATIC ? 'auto' : 'smooth', block: 'start' });
        history.replaceState(null, '', href.slice(hashIdx));
      }
      return;
    }
    if (STATIC || !veil || a.target === '_blank' || /^(mailto:|tel:|http)/.test(href)) return;
    e.preventDefault();
    gsap.to(veil, { scaleX: 1, transformOrigin: 'right', duration: 0.55, ease: 'expo.inOut', onComplete: () => { location.href = href; } });
  });

  /* ---------- liczniki (mono, tabularne) ---------- */
  const fmt = (v, dec) => v.toLocaleString('pl-PL', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  $$('[data-count]').forEach((el) => {
    const end = parseFloat(el.dataset.count), dec = parseInt(el.dataset.decimals || '0', 10);
    if (STATIC) { el.textContent = fmt(end, dec); return; }
    const o = { v: 0 };
    el.textContent = fmt(0, dec);
    gsap.to(o, { v: end, duration: 1.4, ease: 'power3.out', onUpdate: () => { el.textContent = fmt(o.v, dec); }, scrollTrigger: { trigger: el, start: 'top 92%', once: true } });
  });

  /* ---------- hero: dom buduje się ze scrollem ---------- */
  const hero = $('.hero');
  const stageImgs = $$('.plate--hero img[data-stage]');
  const stageCaps = ['rysunek konstrukcji · dzień 0 · wizualizacja', 'stalowy szkielet na płycie · montaż', 'dom gotowy do odbioru · dzień 60 · wizualizacja'];
  const capEl = $('[data-stage-cap]');
  let stage = 0;
  const setStage = (i) => {
    if (i === stage) return;
    stageImgs.forEach((im, j) => gsap.to(im, { opacity: j === i ? 1 : 0, duration: d(0.5), ease: 'power2.out' }));
    if (capEl) capEl.textContent = stageCaps[i];
    stage = i;
  };
  if (hero && stageImgs.length) {
    gsap.set(stageImgs, { position: 'absolute', opacity: 0 });
    gsap.set(stageImgs[0], { opacity: 1 });
    if (STATIC) { setStage(2); }
    else {
      const intro = gsap.timeline({ delay: 0.1 });
      intro.from('.hero__title', { x: -40, opacity: 0, duration: 1.2 }, 0)
        .from('.hero__lead, .hero__actions', { x: -24, opacity: 0, stagger: 0.1, duration: 1 }, 0.15)
        .fromTo('.plate--hero', { clipPath: 'inset(0 0 0 100%)' }, { clipPath: 'inset(0 0 0 0%)', duration: 1.3, ease: 'expo.inOut' }, 0.1)
        .from('.stagebar__fill', { scaleX: 0, duration: 1.4, ease: 'expo.inOut' }, 0.5)
        .from('.stagebar__range', { scaleX: 0, duration: 1, ease: 'expo.inOut' }, 1.1)
        .from('.stagebar__l, .stagebar__seq li', { x: -12, opacity: 0, stagger: 0.05, duration: 0.7 }, 1.3);
      const mm = gsap.matchMedia();
      mm.add('(min-width: 901px)', () => {
        ScrollTrigger.create({
          trigger: hero, start: 'top top', end: '+=120%', pin: true, pinSpacing: true, anticipatePin: 1,
          onUpdate: (s) => setStage(s.progress < 0.3 ? 0 : s.progress < 0.65 ? 1 : 2),
        });
      });
      mm.add('(max-width: 900px)', () => {
        const id = setInterval(() => setStage((stage + 1) % 3), 2600);
        return () => clearInterval(id);
      });
    }
  }

  /* ---------- wykres metrażu ---------- */
  const rows = $$('.mrow');
  if (rows.length) {
    const stageWrap = $('.models__stage');
    const imgs = stageWrap ? $$('img', stageWrap) : [];
    const cap = $('[data-model-cap]');
    let current = imgs.length ? (rows.find((r) => r.classList.contains('is-active'))?.dataset.model || rows[0].dataset.model) : null;
    const show = (slug) => {
      if (!imgs.length || slug === current) return;
      imgs.forEach((im) => im.classList.toggle('is-on', im.dataset.model === slug));
      if (cap) cap.textContent = rows.find((r) => r.dataset.model === slug)?.querySelector('b')?.textContent || '';
      current = slug;
    };
    if (imgs.length) imgs.forEach((im) => im.classList.toggle('is-on', im.dataset.model === current));
    rows.forEach((row) => {
      row.addEventListener('mouseenter', () => show(row.dataset.model));
      row.addEventListener('focus', () => show(row.dataset.model));
      if (isTouch) ScrollTrigger.create({ trigger: row, start: 'top 55%', end: 'bottom 55%', onToggle: (s) => s.isActive && show(row.dataset.model) });
    });
    if (!STATIC) {
      const wrap = $('.mrows');
      gsap.to($$('.mrow__bar', wrap), { scaleX: 1, duration: 1.2, stagger: 0.08, ease: 'expo.inOut', scrollTrigger: { trigger: wrap, start: 'top 80%', once: true } });
      gsap.from($$('.mrow__val', wrap), { opacity: 0, x: -10, duration: 0.6, stagger: 0.08, delay: 0.6, scrollTrigger: { trigger: wrap, start: 'top 80%', once: true } });
    }
  }

  /* ---------- wejścia sekcji (tylko wzdłuż X) ---------- */
  if (!STATIC) {
    $$('.plate').forEach((p) => {
      if (p.classList.contains('plate--hero') || p.closest('.strip__track')) return;
      gsap.fromTo(p, { clipPath: 'inset(0 0 0 100%)' }, { clipPath: 'inset(0 0 0 0%)', duration: 1.2, ease: 'expo.inOut', scrollTrigger: { trigger: p, start: 'top 85%', once: true } });
    });
    $$('.strip__track').forEach((track) => {
      gsap.from(track.children, { x: 80, opacity: 0, duration: 1, stagger: 0.08, scrollTrigger: { trigger: track, start: 'top 85%', once: true } });
    });
  }

  /* ---------- opcje w zamówieniu ---------- */
  const orows = $$('.orow');
  if (orows.length) {
    const imgs = $$('.variants__stage img'), label = $('.variants__label');
    orows.forEach((row, i) => row.addEventListener('click', () => {
      orows.forEach((r) => { r.classList.remove('is-active'); r.setAttribute('aria-selected', 'false'); });
      row.classList.add('is-active'); row.setAttribute('aria-selected', 'true');
      imgs.forEach((im, j) => im.classList.toggle('is-active', j === i));
      if (label) label.textContent = row.dataset.label || '';
      ScrollTrigger.refresh();
    }));
  }

  /* ---------- akordeon specyfikacji ---------- */
  $$('.acc__item').forEach((item) => {
    const btn = $('.acc__btn', item), panel = $('.acc__panel', item);
    btn.addEventListener('click', () => {
      const open = item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
      gsap.to(panel, { height: open ? 'auto' : 0, duration: d(0.6), ease: 'expo.inOut', onComplete: () => ScrollTrigger.refresh() });
    });
  });
  const first = $('.acc__item .acc__btn');
  if (first) first.click();

  /* ---------- lightbox ---------- */
  const lb = $('.lightbox');
  if (lb) {
    const img = $('img', lb), cap = $('figcaption', lb), items = $$('[data-lightbox]');
    let idx = 0;
    const show = (i) => {
      idx = (i + items.length) % items.length;
      gsap.to(img, { opacity: 0, duration: d(0.15), onComplete: () => {
        img.src = items[idx].dataset.lightbox; img.alt = $('img', items[idx])?.alt || '';
        cap.textContent = items[idx].dataset.cap || '';
        gsap.to(img, { opacity: 1, duration: d(0.35) });
      } });
    };
    const open = (i) => { lb.classList.add('is-open'); body.style.overflow = 'hidden'; show(i); $('.lightbox__close', lb).focus(); };
    const close = () => { lb.classList.remove('is-open'); body.style.overflow = ''; };
    items.forEach((el, i) => el.addEventListener('click', () => open(i)));
    $('.lightbox__close', lb).addEventListener('click', close);
    $('.prev', lb).addEventListener('click', () => show(idx - 1));
    $('.next', lb).addEventListener('click', () => show(idx + 1));
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    document.addEventListener('keydown', (e) => {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(idx + 1);
      if (e.key === 'ArrowLeft') show(idx - 1);
    });
  }

  /* ---------- pasek zdjęć: przeciąganie ---------- */
  $$('.strip__track').forEach((strip) => {
    let down = false, startX = 0, startLeft = 0, moved = false;
    strip.addEventListener('pointerdown', (e) => { down = true; moved = false; startX = e.clientX; startLeft = strip.scrollLeft; strip.style.cursor = 'grabbing'; });
    window.addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - startX; if (Math.abs(dx) > 4) moved = true; strip.scrollLeft = startLeft - dx; });
    window.addEventListener('pointerup', () => { down = false; strip.style.cursor = 'grab'; });
    strip.addEventListener('click', (e) => { if (moved) { e.stopPropagation(); e.preventDefault(); } }, true);
  });

  /* ---------- formularz: walidacja + mailto ---------- */
  const form = $('.form-grid');
  if (form) form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = $('#f-name'), email = $('#f-email'), err = $('.form-grid__err');
    const okName = name.value.trim().length > 1, okMail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
    name.setAttribute('aria-invalid', String(!okName)); email.setAttribute('aria-invalid', String(!okMail));
    if (!okName || !okMail) { err.hidden = false; (okName ? email : name).focus(); return; }
    err.hidden = true;
    const f = new FormData(form);
    const subject = encodeURIComponent(`Zapytanie ze strony: ${f.get('projekt') || 'MoVilla'}`);
    const bodyTxt = encodeURIComponent(`Imię i nazwisko: ${f.get('name')}\nE-mail: ${f.get('email')}\nTelefon: ${f.get('phone') || '-'}\nModel: ${f.get('projekt')}\nLokalizacja działki: ${f.get('place') || '-'}\n\n${f.get('msg') || ''}`);
    location.href = `mailto:hello@movilla.pl?subject=${subject}&body=${bodyTxt}`;
  });

  window.addEventListener('load', () => ScrollTrigger.refresh());
})();
