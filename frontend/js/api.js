// ============================================================
//  api.js — Kitchen Stock AI · Central API Layer
//  Change BASE_URL to your FastAPI server address
// ============================================================

const BASE_URL = "http://localhost:8000"; // ← CHANGE THIS if deployed

// ── Generic fetch wrapper ──────────────────────────────────
async function apiFetch(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const config = {
    headers: { "Content-Type": "application/json" },
    ...options,
  };
  try {
    const res = await fetch(url, config);
    const json = await res.json();
    if (!res.ok) {
      throw new Error(json.detail || json.message || `HTTP ${res.status}`);
    }
    return json;
  } catch (err) {
    if (err instanceof TypeError) {
      throw new Error("Cannot connect to backend. Is the server running?");
    }
    throw err;
  }
}

// ── Health ─────────────────────────────────────────────────
export const API = {
  health: () => apiFetch("/health"),

  // Dashboard
  dashboard: () => apiFetch("/dashboard"),

  // Inventory
  getInventory: () => apiFetch("/inventory"),
  addInventory: (item, quantity, unit, expiry_date = null) =>
    apiFetch("/inventory", {
      method: "POST",
      body: JSON.stringify({ item, quantity, unit, expiry_date }),
    }),
  updateInventory: (item_name, quantity) =>
    apiFetch(`/inventory/${encodeURIComponent(item_name)}`, {
      method: "PUT",
      body: JSON.stringify({ quantity }),
    }),
  deleteInventory: (item_name) =>
    apiFetch(`/inventory/${encodeURIComponent(item_name)}`, {
      method: "DELETE",
    }),

  // Alerts
  getAlerts: () => apiFetch("/alerts"),

  // Dishes
  checkDish: (dish_name, servings) =>
    apiFetch("/dishes/check", {
      method: "POST",
      body: JSON.stringify({ dish_name, servings }),
    }),
  cookDish: (dish_name, servings) =>
    apiFetch("/dishes/cook", {
      method: "POST",
      body: JSON.stringify({ dish_name, servings }),
    }),

  // Recipes
  suggestRecipes: (max_missing = 2) =>
    apiFetch("/recipes/suggest", {
      method: "POST",
      body: JSON.stringify({ max_missing }),
    }),

  // Shopping
  getShopping: () => apiFetch("/shopping"),

  // Consumption
  logDish: (dish_name, servings, date) =>
    apiFetch("/consumption/log", {
      method: "POST",
      body: JSON.stringify({ dish_name, servings, date }),
    }),
  getDailyUsage: () => apiFetch("/consumption/daily"),
  estimateUsage: (from_date, to_date) =>
    apiFetch(`/consumption/estimate?from_date=${from_date}&to_date=${to_date}`),

  // Predictions
  getPredictions: () => apiFetch("/predict/runout"),
  getMLPredictions: () => apiFetch("/predict/ml"),

  // Storage
  getStorageAll: () => apiFetch("/storage"),
  getStorage: (item_name) =>
    apiFetch(`/storage/${encodeURIComponent(item_name)}`),
};

export default API;
