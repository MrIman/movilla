/* ==========================================================================
   MOVILLA — main.js (gałąź „nestora”)  GSAP 3.14 + ScrollTrigger
   Zasady: animacje tylko transform/opacity, brak pinowania na dotyku,
   pełne wsparcie prefers-reduced-motion i ?static, brak zależności od kursora.
   ========================================================================== */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches || new URLSearchParams(location.search).has('static');
  const MOTION = hasGsap && !reduce;
  const isTouch = matchMedia('(hover: none), (pointer: coarse)').matches;
  const body = document.body, html = document.documentElement;
  if (new URLSearchParams(location.search).has('capture')) html.classList.add('is-capture');
  if (MOTION) { gsap.registerPlugin(ScrollTrigger); gsap.defaults({ ease: 'power3.out', duration: 1 }); html.classList.add('js-motion'); }

  /* ---------- nawigacja: stan po przewinięciu, chowanie przy scrollu w dół ---------- */
  const nav = $('#nav');
  let lastY = window.scrollY, ticking = false;
  const onScroll = () => {
    const y = window.scrollY;
    nav.classList.toggle('is-solid', y > 24);
    if (!body.classList.contains('menu-open')) nav.classList.toggle('is-hidden', y > lastY + 6 && y > 320);
    if (y < lastY - 6) nav.classList.remove('is-hidden');
    lastY = y;
    $('.mobile-cta')?.classList.toggle('is-on', y > window.innerHeight * 0.6);
    ticking = false;
  };
  window.addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  /* aktywny link */
  const navLinks = $$('.nav__links a');
  if ('IntersectionObserver' in window && navLinks.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        navLinks.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href').endsWith('#' + en.target.id)));
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    $$('main section[id]').forEach((s) => io.observe(s));
  }

  /* ---------- menu mobilne ---------- */
  const menu = $('#menu'), burger = $('.nav__burger');
  const toggleMenu = (open) => {
    const isOpen = open ?? !body.classList.contains('menu-open');
    body.classList.toggle('menu-open', isOpen);
    body.style.overflow = isOpen ? 'hidden' : '';
    burger.setAttribute('aria-expanded', String(isOpen));
    burger.setAttribute('aria-label', isOpen ? 'Zamknij menu' : 'Otwórz menu');
    menu.setAttribute('aria-hidden', String(!isOpen));
    if (isOpen) nav.classList.remove('is-hidden');
  };
  burger?.addEventListener('click', () => toggleMenu());
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && body.classList.contains('menu-open')) { toggleMenu(false); burger.focus(); } });
  matchMedia('(min-width: 900px)').addEventListener('change', (e) => { if (e.matches && body.classList.contains('menu-open')) toggleMenu(false); });

  /* ---------- kotwice (zamykają menu) ---------- */
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    const href = a.getAttribute('href');
    const i = href.indexOf('#');
    if (i < 0) return;
    const sameDoc = i === 0 || href.slice(0, i).split('/').pop() === location.pathname.split('/').pop();
    if (!sameDoc) return;
    const target = document.getElementById(href.slice(i + 1));
    if (!target) return;
    e.preventDefault();
    if (body.classList.contains('menu-open')) toggleMenu(false);
    target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    history.replaceState(null, '', href.slice(i));
  });

  /* ---------- wyjście ze strony: krótkie wygaszenie ---------- */
  if (MOTION) document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || a.target === '_blank') return;
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || /^(mailto:|tel:|http)/.test(href) || href.includes('#')) return;
    e.preventDefault();
    body.classList.add('is-leaving');
    setTimeout(() => { location.href = href; }, 300);
  });
  window.addEventListener('pageshow', (e) => { if (e.persisted) body.classList.remove('is-leaving'); });

  /* ---------- liczniki ---------- */
  const fmt = (v, d) => v.toLocaleString('pl-PL', { minimumFractionDigits: d, maximumFractionDigits: d });
  $$('[data-count]').forEach((el) => {
    const end = parseFloat(el.dataset.count), d = parseInt(el.dataset.decimals || '0', 10);
    el.textContent = fmt(end, d);
    if (!MOTION) return;
    const o = { v: 0 };
    gsap.to(o, { v: end, duration: 1.4, ease: 'power3.out', onUpdate: () => { el.textContent = fmt(o.v, d); }, scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
  });

  /* ---------- animacje wejścia ---------- */
  if (MOTION) {
    /* hero */
    const heroTl = gsap.timeline({ delay: 0.15 });
    heroTl.to('.hero__media img, .phero__media img', { scale: 1, duration: 1.8, ease: 'power2.out' }, 0)
      .to('.hero__title .line', { y: 0, opacity: 1, stagger: 0.1, duration: 1.1, ease: 'power4.out' }, 0.2)
      .to('.hero__aside > *', { opacity: 1, y: 0, stagger: 0.12, duration: 0.9 }, 0.6);
    /* paralaksa hero tylko z myszą (dotyk: brak, bo scroll-jank) */
    if (!isTouch) {
      $$('.hero__media img, .phero__media img, .pnext__media img').forEach((img) => {
        const sec = img.closest('section, a');
        gsap.to(img, { yPercent: 12, ease: 'none', scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom top', scrub: true } });
      });
    }
    /* reveal */
    $$('[data-reveal]').forEach((el) => {
      gsap.to(el, { y: 0, opacity: 1, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
    });
    $$('[data-stagger]').forEach((wrap) => {
      gsap.to(wrap.children, { y: 0, opacity: 1, duration: 0.9, stagger: 0.08, ease: 'power3.out', scrollTrigger: { trigger: wrap, start: 'top 88%', once: true } });
    });
    /* statement: słowa rozjaśniają się ze scrollem */
    const st = $('[data-split]');
    if (st) {
      st.innerHTML = st.textContent.trim().split(/\s+/).map((w) => `<span class="w">${w}</span>`).join(' ');
      gsap.to($$('.w', st), { opacity: 1, stagger: 0.05, ease: 'none', scrollTrigger: { trigger: st, start: 'top 78%', end: 'bottom 48%', scrub: 0.5 } });
    }
    /* karty projektów: lekka paralaksa (tylko z myszą) */
    if (!isTouch) $$('.pj__media, .form__img, .pg__item').forEach((el) => {
      gsap.fromTo(el, { y: 28 }, { y: -28, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: 0.6 } });
    });
    /* obrazy: delikatny zoom-out przy wejściu */
    $$('.pj__img img, .form__img img, .reveal__img img, .pg__img img').forEach((img) => {
      gsap.fromTo(img, { scale: 1.08 }, { scale: 1, duration: 1.4, ease: 'power2.out', scrollTrigger: { trigger: img, start: 'top 92%', once: true } });
    });
    window.addEventListener('load', () => ScrollTrigger.refresh());
  } else {
    $$('[data-split]').forEach((st) => { st.style.opacity = 1; });
  }

  /* ---------- film w tle hero (tylko gdy ruch dozwolony i brak trybu oszczędzania danych) ---------- */
  const heroVideo = $('.hero__video');
  if (heroVideo) {
    const conn = navigator.connection || {};
    const allow = !reduce && !conn.saveData && !/(^|\D)(2g|3g)$/.test(conn.effectiveType || '') && heroVideo.canPlayType('video/mp4');
    const toggle = $('.hero__toggle');
    if (allow) {
      const src = (window.innerWidth < 760 && heroVideo.dataset.srcMobile) ? heroVideo.dataset.srcMobile : heroVideo.dataset.src;
      heroVideo.src = src;
      heroVideo.addEventListener('playing', () => { heroVideo.classList.add('is-ready'); toggle.hidden = false; }, { once: true });
      heroVideo.addEventListener('error', () => { heroVideo.remove(); }, { once: true });
      const tryPlay = () => heroVideo.play().catch(() => {});
      if ('IntersectionObserver' in window) {
        new IntersectionObserver((en) => { en[0].isIntersecting ? (heroVideo.dataset.paused ? null : tryPlay()) : heroVideo.pause(); }, { threshold: 0.1 }).observe(heroVideo);
      } else tryPlay();
      document.addEventListener('visibilitychange', () => { if (document.hidden) heroVideo.pause(); else if (!heroVideo.dataset.paused) tryPlay(); });
      toggle.addEventListener('click', () => {
        const playing = !heroVideo.paused;
        if (playing) { heroVideo.pause(); heroVideo.dataset.paused = '1'; } else { delete heroVideo.dataset.paused; tryPlay(); }
        toggle.setAttribute('aria-pressed', String(!playing));
        toggle.setAttribute('aria-label', playing ? 'Odtwórz film w tle' : 'Zatrzymaj film w tle');
        $('.ic-pause', toggle).toggleAttribute('hidden', playing);
        $('.ic-play', toggle).toggleAttribute('hidden', !playing);
      });
    } else heroVideo.remove();
  }

  /* ---------- zakładki wariantów ---------- */
  const tabs = $$('.tab');
  if (tabs.length) {
    const panels = $$('.tabpanel');
    const select = (i) => {
      tabs.forEach((t, j) => { t.classList.toggle('is-active', j === i); t.setAttribute('aria-selected', String(j === i)); t.tabIndex = j === i ? 0 : -1; });
      panels.forEach((p, j) => { p.hidden = j !== i; p.classList.toggle('is-active', j === i); });
      if (MOTION) gsap.fromTo(panels[i], { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.5 });
      if (MOTION) ScrollTrigger.refresh();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); const n = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length; select(n); tabs[n].focus(); }
      });
    });
    select(0);
  }

  /* ---------- akordeon ---------- */
  $$('.acc__item').forEach((item, i) => {
    const btn = $('.acc__btn', item), panel = $('.acc__panel', item);
    const set = (open, instant) => {
      item.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
      if (MOTION && !instant) gsap.to(panel, { height: open ? 'auto' : 0, duration: 0.5, ease: 'power3.inOut', onComplete: () => ScrollTrigger.refresh() });
      else panel.style.height = open ? 'auto' : '0px';
    };
    btn.addEventListener('click', () => set(!item.classList.contains('is-open')));
    if (i === 0) set(true, true);
  });

  /* ---------- lightbox ---------- */
  const lb = $('.lightbox');
  if (lb) {
    const img = $('img', lb), cap = $('figcaption', lb), items = $$('[data-lightbox]');
    let idx = 0, lastFocus = null;
    const show = (i) => {
      idx = (i + items.length) % items.length;
      img.src = items[idx].dataset.lightbox;
      img.alt = $('img', items[idx])?.alt || '';
      cap.textContent = items[idx].dataset.cap || '';
    };
    const open = (i) => { lastFocus = document.activeElement; lb.hidden = false; body.style.overflow = 'hidden'; show(i); $('.lightbox__close', lb).focus(); };
    const close = () => { lb.hidden = true; body.style.overflow = ''; lastFocus?.focus(); };
    items.forEach((el, i) => {
      el.setAttribute('tabindex', '0'); el.setAttribute('role', 'button'); el.setAttribute('aria-label', 'Powiększ: ' + (el.dataset.cap || 'zdjęcie'));
      el.addEventListener('click', () => open(i));
      el.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } });
    });
    $('.lightbox__close', lb).addEventListener('click', close);
    $('.lightbox__nav--prev', lb).addEventListener('click', () => show(idx - 1));
    $('.lightbox__nav--next', lb).addEventListener('click', () => show(idx + 1));
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    let tx = 0;
    lb.addEventListener('touchstart', (e) => { tx = e.changedTouches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (e) => { const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); }, { passive: true });
    document.addEventListener('keydown', (e) => {
      if (lb.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(idx + 1);
      if (e.key === 'ArrowLeft') show(idx - 1);
    });
  }

  /* ---------- pasek zdjęć: przeciąganie myszą (dotyk ma natywny scroll) ---------- */
  if (!isTouch) $$('.strip').forEach((strip) => {
    let down = false, startX = 0, startLeft = 0, moved = false;
    strip.style.cursor = 'grab';
    strip.addEventListener('pointerdown', (e) => { down = true; moved = false; startX = e.clientX; startLeft = strip.scrollLeft; strip.style.cursor = 'grabbing'; strip.style.scrollSnapType = 'none'; });
    window.addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - startX; if (Math.abs(dx) > 4) moved = true; strip.scrollLeft = startLeft - dx; });
    window.addEventListener('pointerup', () => { if (!down) return; down = false; strip.style.cursor = 'grab'; strip.style.scrollSnapType = ''; });
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
    const bodyTxt = encodeURIComponent(`Imię i nazwisko: ${f.get('name')}\nE-mail: ${f.get('email')}\nTelefon: ${f.get('phone') || '-'}\nProjekt: ${f.get('projekt')}\nLokalizacja działki: ${f.get('place') || '-'}\n\n${f.get('msg') || ''}`);
    location.href = `mailto:hello@movilla.pl?subject=${subject}&body=${bodyTxt}`;
  });
})();
