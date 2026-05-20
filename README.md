<!-- ---
title: Online Shoppers API
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
pinned: false
--- -->

<div align="center">

# 🛒 Online Shoppers Purchase Prediction API

### *DSC × Ureeka Workshop 2026 — Session 2 Starter*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/spaces)

**Turn your trained Session 1 model into a live, public REST API.**

</div>

---

## 🗺️ Big Picture

```
User sends JSON  →  FastAPI validates  →  features.py prepares data  →  model predicts  →  API returns result
```

You don't need to train anything. Your job in Session 2 is to **wrap** the model from Session 1 inside a web service and **deploy** it so anyone can call it from a URL.

---

## 📁 What's Already Here

```
online-shoppers-api/
├── schema.py          ✅  Input & output shape (done — don't change)
├── model.py           ✅  Loads model artifacts (done — don't change)
├── features.py        🔧  Feature engineering — YOU complete this
├── main.py            🔧  API endpoints — YOU complete this
├── requirements.txt   ✅  Python dependencies (done)
├── Dockerfile         ❌  Doesn't exist yet — YOU create this
└── artifacts/
    ├── online_shoppers_model.pkl   ← trained model from Session 1
    ├── threshold.pkl               ← decision threshold (0.49)
    └── model_columns.pkl           ← column order from training
```

> **Rule:** The feature engineering in `features.py` must exactly match what you did in Session 1. If they differ, the model gets wrong data and predictions will be wrong.

---

## ✅ Your To-Do List

Work through these in order.

---

### TODO 1 — `features.py`: Fill in `create_model_features()`

The function skeleton is already there. You need to fill in the body.

This function receives a `ShopperInput` object and must return a `pd.DataFrame` with the **exact same columns** the model was trained on — including all the engineered features from Session 1.

**What to do inside the function:**

```
1. Convert the input to a DataFrame
2. Cast numeric columns to float (use base_numeric_columns)
3. Engineer the same features as Session 1:
      TotalDuration, TotalPages
      ProductDurationPerPage, AdminDurationPerPage, InfoDurationPerPage
      ProductPageRatio, AdminPageRatio, InfoPageRatio
      ProductDurationRatio, AdminDurationRatio, InfoDurationRatio
      AvgDurationPerPage, ExitBounceGap, ExitBounceRatio
      ProductEngagement, DurationWeightedExit, DurationWeightedBounce
      MonthNum (use the MONTH_ORDER dict already defined)
      IsHolidaySeason (Nov or Dec → 1, else → 0)
4. Apply log1p to the columns listed in LOG_COLUMNS
5. Cast categorical code columns to "object" dtype:
      OperatingSystems, Browser, Region, TrafficType, Weekend
6. Reorder columns to match model_columns (already imported)
7. Return the final DataFrame
```

---

### TODO 2 — `main.py`: Add the `/health` endpoint

Add a simple health check that returns `{"status": "ok"}`.

```python
@app.get("/health")
def health():
    # return a dict with status "ok"
```

---

### TODO 3 — `main.py`: Add the `/predict` endpoint

This is the core of the API. Wire everything together.

```python
@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: ShopperInput):
    # 1. Call create_model_features(input_data) → get features DataFrame
    # 2. Call pipeline.predict_proba(features)[:, 1] → get probability
    # 3. Compare probability with best_threshold → get will_purchase (bool)
    # 4. Return PredictionResponse with:
    #       will_purchase, prediction (int), prediction_label (str),
    #       probability (float, rounded to 4 decimals), threshold (float)
```

**Tip — the response label:**
```python
prediction_label = "Will Purchase" if will_purchase else "Will Not Purchase"
```

---

### TODO 4 — Create `Dockerfile`

Create a new file called `Dockerfile` (no extension) in the root folder.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### TODO 5 — Deploy to Hugging Face Spaces

Once everything works locally:

1. Go to [huggingface.co](https://huggingface.co) → log in
2. Click your avatar → **New Space**
3. Name it (e.g. `online-shoppers-api`) → select **Docker** as SDK → set **App Port** to `8000` → Create
4. Upload **only** these files (do **not** upload `venv/`):

```
main.py
schema.py
features.py
model.py
requirements.txt
Dockerfile
artifacts/online_shoppers_model.pkl
artifacts/threshold.pkl
artifacts/model_columns.pkl
```

5. Wait for the build to finish, then open:

```
https://YOUR-USERNAME-YOUR-SPACE-NAME.hf.space/docs
```

✅ **Done** — if Swagger loads and `/health` returns `{"status": "ok"}`, your API is live.

---

## 💻 Local Setup & Running

**1. Create virtual environment**

```powershell
# Windows
py -3.11 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

```bash
# macOS / Linux
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Run the API**

```powershell
# Windows
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

```bash
# macOS / Linux
uvicorn main:app --reload
```

**3. Open Swagger UI**

```
http://localhost:8000/docs
```

---

## 🐳 Test with Docker (before deploying)

> ⚠️ Don't run Docker if your project folder is inside OneDrive — move it to a local path first.

```bash
# Build
docker build -t shoppers-api .

# Run
docker run -p 8000:8000 shoppers-api
```

Open `http://localhost:8000/docs` — if it works, it's ready to deploy.

---

## 🧪 Test the `/predict` Endpoint

Use this sample payload in Swagger UI or via `curl`:

```json
{
  "Administrative": 0,
  "Administrative_Duration": 0,
  "Informational": 0,
  "Informational_Duration": 0,
  "ProductRelated": 5,
  "ProductRelated_Duration": 320.5,
  "BounceRates": 0.02,
  "ExitRates": 0.05,
  "PageValues": 15.3,
  "SpecialDay": 0,
  "Month": "Nov",
  "OperatingSystems": 2,
  "Browser": 2,
  "Region": 1,
  "TrafficType": 2,
  "VisitorType": "Returning_Visitor",
  "Weekend": false
}
```

**Expected response:**

```json
{
  "will_purchase": true,
  "prediction": 1,
  "prediction_label": "Will Purchase",
  "probability": 0.618,
  "threshold": 0.49
}
```

---

## 🔧 Troubleshooting

<details>
<summary><b>PowerShell blocks venv activation</b></summary>

Skip activation — call the venv Python directly:

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --reload
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

</details>

<details>
<summary><b>ModuleNotFoundError</b></summary>

Run:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

</details>

<details>
<summary><b>Artifact not found (.pkl files)</b></summary>

Make sure all three files are inside the `artifacts/` folder:
```
artifacts/online_shoppers_model.pkl
artifacts/threshold.pkl
artifacts/model_columns.pkl
```

</details>

<details>
<summary><b>Predictions seem wrong</b></summary>

The feature engineering in `features.py` must match Session 1 exactly — same column names, same formulas, same order. Compare your `create_model_features()` against the Session 1 notebook.

</details>

---

## 📋 Completion Checklist

```
□  features.py  — create_model_features() fully implemented
□  main.py      — /health endpoint added
□  main.py      — /predict endpoint added and working
□  Dockerfile   — created
□  Local test   — uvicorn runs, /docs loads, /predict returns correct JSON
□  Docker test  — docker build + run works (optional but recommended)
□  Deployed     — files uploaded to Hugging Face Spaces
□  Public URL   — /docs and /health accessible from your Space URL  🎉
```

---

<div align="center">

*Built for **DSC × Ureeka Workshop 2026** · Session 2: Beyond the Model*

</div>
