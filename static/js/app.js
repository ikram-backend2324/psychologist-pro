/* Ruhiyat — interactions & animation */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* storage unavailable */ } },
  };
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Theme */
  const root = document.documentElement;
  $$("[data-theme-toggle]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      store.set("theme", next);
    })
  );

  /* Navbar shadow on scroll */
  const nav = $(".nav");
  const onScroll = () => nav && nav.classList.toggle("scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Drawer */
  const drawer = $(".drawer");
  $$("[data-drawer-open]").forEach((b) => b.addEventListener("click", () => drawer.classList.add("open")));
  $$("[data-drawer-close]").forEach((b) => b.addEventListener("click", () => drawer.classList.remove("open")));

  /* Dropdowns */
  $$(".dropdown").forEach((dd) => {
    const trigger = $("[data-dropdown]", dd);
    trigger.addEventListener("click", (e) => {
      e.stopPropagation();
      $$(".dropdown.open").forEach((o) => o !== dd && o.classList.remove("open"));
      dd.classList.toggle("open");
    });
  });
  document.addEventListener("click", () => $$(".dropdown.open").forEach((o) => o.classList.remove("open")));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      $$(".dropdown.open").forEach((o) => o.classList.remove("open"));
      drawer && drawer.classList.remove("open");
    }
  });

  /* Toasts */
  $$(".toast").forEach((t, i) => {
    const close = () => { t.classList.add("hide"); setTimeout(() => t.remove(), 400); };
    $("button", t).addEventListener("click", close);
    setTimeout(close, 6000 + i * 800);
  });

  /* Reveal on scroll */
  const reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("in"));
  }

  /* Count-up numbers */
  const counters = $$("[data-count]");
  const runCount = (el) => {
    const target = parseInt(el.dataset.count, 10) || 0;
    if (reduceMotion || target === 0) { el.textContent = target; return; }
    const dur = 1400, t0 = performance.now();
    const tick = (now) => {
      const p = Math.min(1, (now - t0) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ("IntersectionObserver" in window && !reduceMotion) {
    counters.forEach((c) => { c.textContent = "0"; });
    const co = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { runCount(en.target); co.unobserve(en.target); }
    }));
    counters.forEach((c) => co.observe(c));
  } else counters.forEach(runCount);

  /* Tilt cards (pointer devices only) */
  if (!reduceMotion && window.matchMedia("(hover: hover)").matches) {
    $$(".tilt").forEach((card) => {
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(900px) rotateX(${-y * 6}deg) rotateY(${x * 8}deg) translateY(-6px)`;
      });
      card.addEventListener("pointerleave", () => { card.style.transform = ""; });
    });
  }

  /* Register: role picker reveals psychologist fields */
  const roleInputs = $$('input[name="role"]');
  if (roleInputs.length) {
    const sync = () => {
      const psych = roleInputs.some((i) => i.checked && i.value === "psychologist");
      $$(".psych-only").forEach((el) => el.classList.toggle("show", psych));
      $$(".client-only").forEach((el) => el.classList.toggle("hide", psych));
    };
    roleInputs.forEach((i) => i.addEventListener("change", sync));
    sync();
  }

  /* Quiz: enable submit when everything is answered */
  const quiz = $("[data-quiz]");
  if (quiz) {
    const groups = $$(".question", quiz);
    const counter = $(".quiz-counter b", quiz);
    const submit = $("button[type=submit]", quiz);
    const update = () => {
      const answered = groups.filter((g) => $("input:checked", g)).length;
      if (counter) counter.textContent = answered;
      submit.disabled = answered < groups.length;
    };
    quiz.addEventListener("change", (e) => {
      update();
      const q = e.target.closest(".question");
      const next = q && q.nextElementSibling;
      if (next && next.classList.contains("question") && !$("input:checked", next)) {
        setTimeout(() => next.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" }), 250);
      }
    });
    update();
  }

  /* Breathing game */
  const breath = $("[data-breath]");
  if (breath) {
    const circle = $(".breath-circle", breath);
    const phaseEl = $(".phase", breath);
    const dots = $$(".breath-dots i", breath);
    const startBtn = $("[data-breath-start]", breath);
    const finishBtn = $("[data-breath-finish]");
    const ds = breath.dataset;
    const labels = { inhale: ds.lInhale, hold: ds.lHold, exhale: ds.lExhale, done: ds.lDone };
    const t = { inhale: +breath.dataset.inhale, hold: +breath.dataset.hold, exhale: +breath.dataset.exhale };
    const cycles = +breath.dataset.cycles;
    let running = false;
    const wait = (s) => new Promise((r) => setTimeout(r, s * 1000));
    const countdown = async (label, secs) => {
      for (let i = secs; i > 0; i--) { circle.textContent = `${label} · ${i}`; await wait(1); }
    };
    startBtn.addEventListener("click", async () => {
      if (running) return;
      running = true;
      startBtn.disabled = true;
      for (let c = 0; c < cycles; c++) {
        phaseEl.textContent = labels.inhale;
        circle.style.setProperty("--dur", t.inhale + "s");
        circle.classList.add("grow");
        await countdown(labels.inhale, t.inhale);
        if (t.hold) { phaseEl.textContent = labels.hold; await countdown(labels.hold, t.hold); }
        phaseEl.textContent = labels.exhale;
        circle.style.setProperty("--dur", t.exhale + "s");
        circle.classList.remove("grow");
        await countdown(labels.exhale, t.exhale);
        dots[c] && dots[c].classList.add("on");
      }
      phaseEl.textContent = labels.done;
      circle.textContent = "✓";
      running = false;
      startBtn.disabled = false;
      if (finishBtn) { finishBtn.disabled = false; finishBtn.classList.add("btn-primary"); }
      burst(60);
    });
  }

  /* Flip cards: all flipped → continue */
  const flipGrid = $("[data-flip-grid]");
  if (flipGrid) {
    const cards = $$(".flip", flipGrid);
    const finishBtn = $("[data-flip-finish]");
    const seen = new Set();
    cards.forEach((card, i) => card.addEventListener("click", () => {
      card.classList.toggle("flipped");
      seen.add(i);
      if (seen.size === cards.length && finishBtn && finishBtn.disabled) {
        finishBtn.disabled = false;
        burst(40);
      }
    }));
  }

  /* Reflection: show thinking state while AI responds */
  $$("[data-reflection]").forEach((form) => form.addEventListener("submit", () => {
    const btn = $("button[type=submit]", form);
    const ai = $('input[name="ai"]', form);
    if (btn) { btn.disabled = true; if (ai && ai.checked) btn.innerHTML = `<span class="loading-dots">${btn.dataset.thinking}</span>`; }
  }));

  /* Pause dialog with quick time picks */
  $$("[data-dialog-open]").forEach((b) => b.addEventListener("click", () => {
    const d = document.getElementById(b.dataset.dialogOpen);
    if (d && d.showModal) d.showModal();
  }));
  $$("dialog.modal").forEach((d) => {
    d.addEventListener("click", (e) => { if (e.target === d) d.close(); });
    $$("[data-dialog-close]", d).forEach((b) => b.addEventListener("click", () => d.close()));
  });
  const pad = (n) => String(n).padStart(2, "0");
  const toLocalInput = (dt) => `${dt.getFullYear()}-${pad(dt.getMonth() + 1)}-${pad(dt.getDate())}T${pad(dt.getHours())}:${pad(dt.getMinutes())}`;
  $$("[data-quick]").forEach((b) => b.addEventListener("click", () => {
    const now = new Date();
    const dt = new Date(now);
    const kind = b.dataset.quick;
    if (kind === "evening") { dt.setHours(20, 0, 0, 0); if (dt <= now) dt.setDate(dt.getDate() + 1); }
    if (kind === "tomorrow") { dt.setDate(dt.getDate() + 1); dt.setHours(9, 0, 0, 0); }
    if (kind === "3days") { dt.setDate(dt.getDate() + 3); dt.setHours(19, 0, 0, 0); }
    const input = b.closest("form").querySelector('input[type="datetime-local"]');
    input.value = toLocalInput(dt);
    $$("[data-quick]", b.closest("form")).forEach((x) => x.classList.toggle("on", x === b));
  }));
  $$('input[type="datetime-local"][data-min-now]').forEach((input) => {
    const soon = new Date(Date.now() + 15 * 60000);
    input.min = toLocalInput(soon);
    if (!input.value) {
      const d = new Date(); d.setDate(d.getDate() + 1); d.setHours(9, 0, 0, 0);
      input.value = toLocalInput(d);
    }
  });

  /* Confetti */
  const canvas = $("#confetti");
  function burst(count) {
    if (!canvas || reduceMotion) return;
    const ctx = canvas.getContext("2d");
    const W = (canvas.width = window.innerWidth), H = (canvas.height = window.innerHeight);
    const colors = ["#6c47ff", "#b05cff", "#ff7ab6", "#14b8a6", "#f59e0b", "#22d3ee"];
    const parts = Array.from({ length: count }, () => ({
      x: W / 2 + (Math.random() - 0.5) * W * 0.4, y: H * 0.35, vx: (Math.random() - 0.5) * 14, vy: -Math.random() * 14 - 4,
      s: 6 + Math.random() * 6, r: Math.random() * Math.PI, vr: (Math.random() - 0.5) * 0.3, c: colors[(Math.random() * colors.length) | 0],
    }));
    let frame = 0;
    (function draw() {
      ctx.clearRect(0, 0, W, H);
      parts.forEach((p) => {
        p.vy += 0.35; p.vx *= 0.99; p.x += p.vx; p.y += p.vy; p.r += p.vr;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.fillStyle = p.c;
        ctx.fillRect(-p.s / 2, -p.s / 4, p.s, p.s / 2); ctx.restore();
      });
      if (++frame < 180) requestAnimationFrame(draw); else ctx.clearRect(0, 0, W, H);
    })();
  }

  /* Confirm before submitting forms marked with data-confirm */
  $$("form[data-confirm]").forEach((f) => f.addEventListener("submit", (e) => {
    if (!window.confirm(f.dataset.confirm)) e.preventDefault();
  }));

  /* Filter chips submit their form right away */
  $$("[data-autosubmit]").forEach((input) => input.addEventListener("change", () => input.form.submit()));

  /* Segmented control (tests & games hub) with sliding glider */
  const seg = $("[data-seg]");
  if (seg) {
    const glider = $(".seg-glider", seg);
    const items = $$("[data-seg-items] [data-group]");
    const move = (btn) => {
      glider.style.width = btn.offsetWidth + "px";
      glider.style.transform = `translateX(${btn.offsetLeft - 5}px)`;
    };
    const buttons = $$("button", seg);
    buttons.forEach((btn) => btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.toggle("on", b === btn));
      move(btn);
      const f = btn.dataset.filter;
      items.forEach((el, i) => {
        const show = f === "all" || el.dataset.group === f;
        el.classList.toggle("is-hidden", !show);
        el.classList.remove("pop-in");
        if (show) { el.classList.add("in"); void el.offsetWidth; el.style.animationDelay = (i % 6) * 40 + "ms"; el.classList.add("pop-in"); }
      });
    }));
    requestAnimationFrame(() => move($("button.on", seg)));
    window.addEventListener("resize", () => move($("button.on", seg)));
  }

  /* Mood check-in without reloading */
  const moodForm = $("[data-mood-form]");
  if (moodForm) {
    moodForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = e.submitter;
      if (!btn) return;
      const body = new FormData(moodForm);
      body.set("mood", btn.value);
      try {
        const r = await fetch(moodForm.action, { method: "POST", body, headers: { "X-Requested-With": "fetch" } });
        if (!r.ok) throw new Error();
        $$(".mood-btn", moodForm).forEach((b) => b.classList.toggle("on", b === btn));
        const thanks = $("[data-mood-thanks]");
        if (thanks) thanks.hidden = false;
        const bars = $$(".mood-chart .mood-col", moodForm.parentElement);
        const today = bars[bars.length - 1];
        if (today) {
          const bar = $(".bar", today);
          bar.className = "bar m" + btn.value;
          bar.style.setProperty("--h", btn.value * 20 + "%");
          $(".day", today).textContent = $(".e", btn).textContent;
        }
        if (+btn.value >= 4) burst(40);
      } catch (err) {
        moodForm.submit();
      }
    });
  }

  /* Chat: send without reload, poll for new messages */
  const chat = $("[data-chat]");
  if (chat) {
    const list = $("[data-chat-list]", chat);
    const form = $("[data-chat-form]");
    let lastId = +chat.dataset.lastId || 0;
    const toBottom = () => { chat.scrollTop = chat.scrollHeight; };
    const append = (html, id) => {
      if (!html) return;
      const empty = $("[data-chat-empty]", chat);
      if (empty) empty.remove();
      const tmp = document.createElement("div");
      tmp.innerHTML = html;
      Array.from(tmp.children).forEach((node) => {
        if (!$(`[data-id="${node.dataset.id}"]`, list)) list.appendChild(node);
      });
      lastId = Math.max(lastId, id || 0);
      toBottom();
    };
    toBottom();
    if (form) {
      const ta = $("textarea", form);
      const grow = () => { ta.style.height = "auto"; ta.style.height = Math.min(ta.scrollHeight, 160) + "px"; };
      ta.addEventListener("input", grow);
      ta.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey && window.matchMedia("(hover: hover)").matches) {
          e.preventDefault();
          form.requestSubmit();
        }
      });
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const body = new FormData(form);
        if (e.submitter && e.submitter.name === "topic") body.set("topic", e.submitter.value);
        if (!body.get("text").trim() && !body.get("topic")) return;
        const sendBtn = $(".send-btn", form);
        sendBtn.disabled = true;
        try {
          const r = await fetch(form.action, { method: "POST", body, headers: { "X-Requested-With": "fetch" } });
          const data = await r.json();
          if (r.ok) { append(data.html, data.last_id); ta.value = ""; grow(); }
        } catch (err) {
          form.submit();
        } finally {
          sendBtn.disabled = false;
          ta.focus();
          $$(".dropdown.open").forEach((o) => o.classList.remove("open"));
        }
      });
    }
    const statusEl = $("[data-chat-status]");
    const initialStatus = chat.dataset.status;
    const poll = async () => {
      if (document.hidden) return;
      try {
        const r = await fetch(`${chat.dataset.pollUrl}?after=${lastId}`, { headers: { "X-Requested-With": "fetch" } });
        if (!r.ok) return;
        const data = await r.json();
        append(data.html, data.last_id);
        if (data.status !== initialStatus) window.location.reload();
      } catch (err) { /* offline: try again on the next tick */ }
    };
    if (statusEl) setInterval(poll, 4000);
  }

  /* Situation game: choose a reaction, see feedback, move on */
  const scenario = $("[data-scenario]");
  if (scenario) {
    const cards = $$("[data-scn]", scenario);
    const dots = $$(".scn-dots i", scenario);
    const finish = $("[data-scn-finish]");
    const L = scenario.dataset;
    let good = 0;
    cards.forEach((card, idx) => {
      const opts = $$(".scn-opt", card);
      const result = $(".scn-result", card);
      opts.forEach((opt) => opt.addEventListener("click", () => {
        const pts = +opt.dataset.points, max = +opt.dataset.max;
        const tone = pts >= max && max > 0 ? "great" : pts > 0 ? "ok" : "bad";
        if (tone === "great") good++;
        opts.forEach((o) => { o.disabled = true; if (o !== opt) o.classList.add("dim"); });
        opt.classList.add(tone);
        result.className = "scn-result " + tone;
        $("[data-scn-verdict]", result).textContent = tone === "great" ? L.lGreat : tone === "ok" ? L.lOk : L.lBad;
        $("[data-scn-feedback]", result).textContent = opt.dataset.feedback || "";
        result.hidden = false;
        if (dots[idx]) dots[idx].classList.add("done");
        if (tone === "great") burst(30);
        const next = $(".scn-next", card);
        if (next) { next.hidden = false; next.focus(); }
        else {
          const summary = $(".scn-summary", scenario);
          $("[data-scn-score]", summary).textContent = `${good} / ${cards.length}`;
          setTimeout(() => { summary.hidden = false; summary.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" }); }, 600);
          if (finish) { finish.disabled = false; }
        }
      }));
      const next = $(".scn-next", card);
      if (next) next.addEventListener("click", () => {
        card.hidden = true;
        cards[idx + 1].hidden = false;
        if (dots[idx + 1]) dots[idx + 1].classList.add("on");
        cards[idx + 1].scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
      });
    });
  }

  if (canvas && canvas.dataset.auto) { setTimeout(() => burst(160), 300); setTimeout(() => burst(90), 1100); }
})();
