<div align="center">

# 🍲 Kitchen Stock AI

**Smart Kitchen Inventory & Grocery Planning System**

`Python` · `Rule-Based + ML` · `JSON/SQLite` · `8-Week Build`

---

</div>

## The Problem

Most households track groceries by memory. No structured system, no consumption visibility — so people run out of essentials mid-cook, buy duplicates, or let food expire unused. Working professionals, bachelors, and small families feel this most: career + household, with zero bandwidth for manual tracking.

**Kitchen Stock AI** is a digital kitchen assistant that tracks what's in your kitchen, learns how you actually cook, and tells you what's about to run out — before you find out the hard way, mid-recipe.

---

## ⚡ Quick Facts

| | |
|---|---|
| **Build philosophy** | 70% rule-based, 30% ML — only where ML actually earns its keep |
| **Time to working system** | 4 weeks |
| **Time to intelligent system** | 8 weeks |
| **Total code (estimated)** | ~500 lines |
| **External dependencies** | 2 — `pandas`, `scikit-learn` |

> **The core principle:** don't overthink it. Build something that works, then improve it. By Week 4 there's a working system. By Week 8 it's an intelligent one.

---

## 🧩 Features

<details open>
<summary><b>📦 Inventory & Tracking</b></summary>
<br>

- **Automatic Ingredient Deduction** — log a cooked dish + servings, the system deducts ingredients via dish–ingredient mappings
- **Automatic Mode** — forgot to log? System estimates usage from historical patterns + your cooking profile, so tracking never goes stale
- **Low-Stock Alerts** — real-time threshold monitoring with in-app notifications
- **Expiry Tracking** — flags ingredients nearing expiration to cut food waste
- **Grocery Bill Scanning** — snap a receipt, inventory updates itself

</details>

<details open>
<summary><b>🧠 Personalization & Intelligence</b></summary>
<br>

- **Cooking Profile Onboarding** — short interactive setup to capture household cooking style (spice levels, oil usage, ingredient preferences) for more accurate consumption estimates
- **Behavior-Based Learning** — analyzes cooking history to surface insights (e.g. *"haven't made biryani in a while — want to?"*)
- **Smart Dish Preparation Assistant** — enter a dish, system checks it against current inventory, lists what's missing, and walks through the recipe

</details>

<details open>
<summary><b>🛒 Shopping & Planning</b></summary>
<br>

- **Shopping Mode** — categorized shopping list: finished items, about-to-run-out items, and predicted future needs
- **Recipe Suggestions** — generated from what's currently available, no extra purchases needed
- **Shared Household Access** — multiple family members manage one shared inventory

</details>

<details open>
<summary><b>🛠️ Reliability Layer</b></summary>
<br>

- **Smart Inventory Awareness & Correction** — detects when a user cooks despite the system predicting insufficient stock, infers an unlogged purchase happened, and prompts a manual correction
- **Smart Storage Recommendation** — flags whether an ingredient belongs in the fridge or at room temperature, based on food-storage best practices

</details>

---

## 🔁 The Self-Correction Loop

A real edge case this system explicitly handles: **inventory drifting out of sync with reality.**

```
1. System predicts: "insufficient rice to cook this dish"
2. User cooks it anyway (they bought more rice, just didn't log it)
3. System detects the mismatch between prediction and behavior
4. System infers an external purchase happened
5. System nudges: "Inventory looks outdated — update it?"
```

This keeps predictions trustworthy without demanding perfect manual discipline from the user.

---

## 🏗️ Architecture — 3 Modules, Not 10

<div align="center">

| Module | Purpose | Approach | Complexity |
|---|---|---|:---:|
| **1. Inventory Manager** | Track what's in the kitchen | Database + forms | ⭐ |
| **2. Consumption Tracker** | Learn what gets used and how often | Rules + aggregation | ⭐⭐ |
| **3. Prediction & Suggestion** | Predict run-out dates, suggest recipes | Rules (Phase 1) → ML (Phase 2) | ⭐⭐⭐ |

</div>

**Why so few modules?** Most "smart kitchen" features people assume need ML — reorder timing, recipe suggestion, behavior learning — are actually just clean rule-based logic. Only **consumption prediction** genuinely benefits from ML. Everything else is arithmetic and `if` statements wearing a smart-system costume, and that's fine.

---

## 🗺️ Phased Rollout

<div align="center">

```
PHASE 1 — Weeks 1-4  →  Working inventory system        →  NO ML
PHASE 2 — Weeks 5-8  →  Smart, personalized predictions  →  ML (Linear Regression)
PHASE 3 — Weeks 9+   →  Advanced learning + optimization →  ML (Deep patterns)
```

</div>

| Week | Milestone |
|---|---|
| 1–2 | Inventory pipeline works — add, deduct, view |
| 3–4 | System predicts run-out dates, suggests recipes, builds shopping lists |
| 5–6 | System learns — tracks cooking frequency, personalizes suggestions |
| 7–8 | ML model trained — predictions get measurably more accurate |

No throwaway code — every Phase 1 module carries forward into Phase 3. ML is an upgrade bolted onto existing modules, not a rewrite.

---

## 🎯 Real vs. Simulated (Honest Build Notes)

<table>
<tr>
<td valign="top" width="50%">

**✅ Real**
- Inventory tracking (actual DB)
- Consumption logging (actual user input)
- Predictions (actual math)
- Recipe database
- User testing

</td>
<td valign="top" width="50%">

**⚠️ Simulated (early on)**
- Baseline consumption estimates
- Seed/bootstrap behavior data
- Seasonal variation (added once real data exists)

</td>
</tr>
</table>

---

## 🧰 Tech Stack

```
Language     Python 3.8+
Storage      JSON  →  SQLite (when it outgrows JSON)
ML           scikit-learn (Phase 2 onward)
Web          Flask (Phase 3, optional)
```

---

## 📁 Repository Structure

```
kitchen-stock-ai/
├── modules/
│   ├── inventory_manager.py
│   ├── consumption_tracker.py
│   └── prediction_engine.py
├── data/
│   └── baseline.json
├── app.py
├── requirements.txt
└── README.md
```

---

## 💼 Resume Description

> Designed Kitchen Stock AI, a smart kitchen inventory and grocery planning system combining rule-based logic and ML-driven consumption prediction, featuring automatic ingredient deduction, behavior-based learning, and a self-correcting inventory awareness system.

---

<div align="center">

**Built by [Nithish Kumar](https://github.com/nithishkumar-dev-10)**

</div>
