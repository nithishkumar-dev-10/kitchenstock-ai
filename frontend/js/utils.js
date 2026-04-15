// ============================================================
//  utils.js — Shared helpers across all pages
// ============================================================

// Toast notification system
export function showToast(message, type = "success") {
  const existing = document.getElementById("toast-container");
  if (!existing) {
    const div = document.createElement("div");
    div.id = "toast-container";
    document.body.appendChild(div);
  }
  const toast = document.createElement("div");
  toast.className = `toast toast--${type}`;
  toast.innerHTML = `
    <span class="toast__icon">${type === "success" ? "✓" : type === "error" ? "✕" : "⚠"}</span>
    <span class="toast__msg">${message}</span>
  `;
  document.getElementById("toast-container").appendChild(toast);
  requestAnimationFrame(() => toast.classList.add("toast--show"));
  setTimeout(() => {
    toast.classList.remove("toast--show");
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

// Format date to YYYY-MM-DD
export function todayISO() {
  return new Date().toISOString().split("T")[0];
}

// Status badge HTML
export function statusBadge(status) {
  const map = {
    critical: ["🔴", "critical"],
    warning: ["🟡", "warning"],
    safe: ["🟢", "safe"],
    unknown: ["⚪", "unknown"],
    low_stock: ["🟡", "warning"],
    out_of_stock: ["🔴", "critical"],
  };
  const [icon, cls] = map[status] || ["⚪", "unknown"];
  return `<span class="badge badge--${cls}">${icon} ${status.replace("_", " ")}</span>`;
}

// Set loading state on a button
export function setLoading(btn, loading) {
  if (loading) {
    btn.dataset.originalText = btn.textContent;
    btn.innerHTML = `<span class="spinner"></span> Loading…`;
    btn.disabled = true;
  } else {
    btn.textContent = btn.dataset.originalText || "Submit";
    btn.disabled = false;
  }
}

// Animate a number counter
export function animateCount(el, target, duration = 1000) {
  const start = performance.now();
  const from = parseFloat(el.textContent) || 0;
  function step(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = (from + (target - from) * eased).toFixed(0);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// Render an empty state
export function emptyState(container, message = "No data available") {
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-state__icon">⬛</div>
      <p>${message}</p>
    </div>
  `;
}

// Format quantity with unit
export function formatQty(qty, unit) {
  return `${parseFloat(qty).toFixed(1)} <span class="unit">${unit || ""}</span>`;
}

// Check backend connection and show status
export async function checkConnection(API) {
  const dot = document.getElementById("connection-dot");
  const label = document.getElementById("connection-label");
  try {
    await API.health();
    if (dot) dot.className = "conn-dot conn-dot--online";
    if (label) label.textContent = "Backend Connected";
  } catch {
    if (dot) dot.className = "conn-dot conn-dot--offline";
    if (label) label.textContent = "Backend Offline";
  }
}
