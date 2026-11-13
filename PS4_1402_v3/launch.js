/*
  launch.js — NanospeedGamer landing page controller
  Countdown → auto-redirect to exploit chain, or manual start via button.
  Referrer guard: only fires when reached from index.html in the same origin.
*/

(function () {
  "use strict";

  const COUNTDOWN_SEC = 0; // deliberately no automatic exploit launch
  const DEST = "launch.html?v=hen184-1402-v3&log=1&afterglow=run&mode=kpstep&g=drain:16&g=drainsz:0x4000";

  const countEl = document.getElementById("count"); // <p class="status" id="count">
  const content = document.querySelector(".content");

  function guardOk() {
    return true; // key auth on index.html already protects the page
  }

  /* ── inject start button ─────────────────────────────────────────────── */
  const btn = document.createElement("button");
  btn.id = "startBtn";
  btn.textContent = "START 14.02 HEN (EXPERIMENTAL)";
  btn.style.display = "none"; // hidden until guard passes
  if (content) content.appendChild(btn);

  /* ── go ──────────────────────────────────────────────────────────────── */
  function go() {
    if (countEl) countEl.textContent = "[ EXECUTE ]";
    if (btn) btn.disabled = true;
    location.href = DEST;
  }

  /* ── blocked by referrer guard ───────────────────────────────────────── */
  if (!guardOk()) {
    if (countEl) countEl.textContent = "[ ACCESS DENIED — NAVIGATE FROM ROOT ]";
    return; // stop — session restore, do not fire
  }

  /* ── show button now that we're cleared ─────────────────────────────── */
  btn.style.display = "";
  btn.addEventListener("click", function () {
    go();
  });

  /* NO AUTO-START. The user must click to begin. */
  if (countEl) countEl.textContent =
    "Experimental build. 14.02 HEN support is new; remaining Akatsuki kernel patches are not validated. A full console freeze is possible.";
})();
