# Kubera — expense + crypto tracker

## 👤 Author & Links

**Krupa Koushik (Kouza)**  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Krupa%20Koushik-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/krupa-koushik-kona-355708296/)  
[![X](https://img.shields.io/badge/X-@krupakoushikk-111?logo=x&logoColor=white)](https://x.com/krupakoushikk)


[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](#)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000.svg?logo=flask&logoColor=white)](#)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqlite&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](#contributing)

a minimal personal finance app with:
- 💸 **expense tracker** (+ custom categories)
- ₿ **crypto portfolio** (live prices via CoinGecko)
- 🧾 **trade ledger** (FIFO PnL + holdings)
- 🔐 auth + per‑user data

> built with Flask + SQLite. inspired by CoinGecko’s clean portfolio UX.

---

## ✨ screenshots

| portfolio | trades | modal (buy/sell) |
| --- | --- | --- |
| ![portfolio](images/image1.png) | ![trades](images/image2.png) | ![modal](images/image3.png) |

> add more as you like. files live under `images/`.

---

## 🧱 features

- categories CRUD (per user)
- add/edit/delete transactions
- add coins from CoinGecko search/trending
- per‑coin holdings with **FIFO** unrealized/realized PnL
- trade page with FIFO PnL per sell, average cost, totals
- simple caching for market data (Pro key optional)

---

## 🗺️ roadmap

- 📊 budgeting per category (monthly caps + alerts)
- 🎯 savings goals (time‑bound plans, progress bars)
- 📈 visualizations (pandas/matplotlib or Chart.js)
- 🧠 “insights” (OpenAI) — spending patterns, goal nudges, basic investing hygiene
- 🔔 email/Discord/webhook notifications

---

## 🚀 quickstart

```bash
# 1) clone
git clone https://github.com/<you>/kubera.git
cd kubera

# 2) create venv
python -m venv .venv
# windows: .venv\Scripts\activate
source .venv/bin/activate

# 3) install
pip install -r requirements.txt

# 4) env
cp .env.example .env
# fill values (see below)

# 5) run
flask --app main.py --debug run
# app: http://127.0.0.1:5000
