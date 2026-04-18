# 🍳 KitchenIQ — Smart Kitchen Inventory AI

> An AI-powered kitchen management system that tracks ingredients, predicts consumption, and keeps your pantry one step ahead.

---

## 🚀 Features

- 📦 **Real-time Ingredient Tracking** — Know exactly what's in your kitchen at any moment
- 🔄 **Auto Consumption Estimation** — Learns your usage patterns and auto-deducts stock
- 👤 **Personalized Cooking Profile** — Adapts to your dietary preferences and meal habits
- 🔔 **Low Stock Alerts** — Get notified before you run out of essentials
- 🛒 **Smart Grocery Suggestions** — AI recommends what to buy based on your patterns
- 🍽️ **Recipe Suggestions** — Get meal ideas based on what you currently have

---

## 🧠 How It Works

```
User Inputs / Meal Logs
        ↓
  Inventory Engine
  (tracks stock levels)
        ↓
  AI Consumption Model
  (predicts usage trends)
        ↓
  Alert & Suggestion Layer
  (low stock + grocery list)
```

---

## 🛠️ Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Backend    | Python / FastAPI    |
| AI Engine  | Gemini API          |
| Storage    | JSON / SQLite       |
| Frontend   | HTML, CSS, JS       |

---

## 📁 Project Structure

```
kitcheniq/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── ai_engine.py         # Gemini AI integration
│   ├── inventory.py         # Stock tracking logic
│   ├── consumption_model.py # Usage prediction
│   └── alert_engine.py      # Low stock & notifications
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── data/
│   └── inventory.json       # Persistent ingredient store
├── requirements.txt
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/kitcheniq.git
cd kitcheniq
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

```bash
export GEMINI_API_KEY="your_key_here"
```

### 4. Run the backend

```bash
uvicorn backend.main:app --reload
```

### 5. Open the frontend

Open `frontend/index.html` in your browser or serve it locally.

---

## 📡 API Endpoints

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| GET    | `/inventory`          | Get current stock levels       |
| POST   | `/inventory/add`      | Add or update an ingredient    |
| POST   | `/inventory/consume`  | Log ingredient usage           |
| GET    | `/alerts`             | Get low stock alerts           |
| GET    | `/suggestions`        | Get AI grocery suggestions     |
| GET    | `/recipes`            | Get recipe ideas from stock    |

---

## 💡 Example Use Case

> You cook pasta twice a week. KitchenIQ learns this, auto-deducts spaghetti and sauce from your inventory, and sends you a grocery alert before you hit zero — without you lifting a finger.

---

## 🗺️ Roadmap

- [x] Inventory tracking core
- [x] AI-powered consumption estimation
- [x] Low stock alerts
- [ ] Voice input support
- [ ] Mobile app (React Native)
- [ ] Barcode scanner integration
- [ ] Multi-user household support

---

## 👨‍💻 Built By

**Nithish Kumar S** — First-year CS undergrad building real-world AI products.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/your-username)

---

## 📄 License

MIT License — feel free to use, fork, and build on it.
