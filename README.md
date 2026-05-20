---
title: Online Shoppers API
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
pinned: false
---

# Online Shoppers Purchase Prediction API

This is the Session 2 deployment project.

In Session 1, we trained a machine learning model. In Session 2, we turn that trained model into a small web service, so other people can send shopper-session data and receive a prediction.

The prediction answers this question:

```text
Based on this visitor's session, is the visitor likely to purchase?
```

## Big Picture
Think of the project like a restaurant:

```text
Customer order -> Kitchen prepares food -> Waiter returns result
```

In this project:

```text
User input -> FastAPI receives it -> features.py prepares it -> model predicts -> API returns result
```

The user does not need to know how the model works internally. They only send normal input data, and the API handles the rest.

## Folder Contents

```text
main.py                  The FastAPI app. This is the front door of the API.
schema.py                Describes what input the API accepts and what output it returns.
features.py              Recreates the feature engineering from Session 1.(turns raw input into model-ready columns)
model.py                 Loads the trained model, threshold, and column order.
online_shoppers_model.pkl  The trained machine learning model from Session 1.(artifact)
threshold.pkl            The decision threshold from Session 1. (artifact)
model_columns.pkl        The exact column order used during training.(artifact)
requirements.txt         The Python packages needed to run the API.
Dockerfile               Instructions for packaging the API with Docker.
.dockerignore            Tells Docker which local files should not be packed.
```
## Recommended Code-Building Flow
This is the recommended order if building the project from scratch.

1. requirements.txt
2. schema.py
3. features.py
4. model.py
5. main.py
6. Dockerfile
7. .dockerignore
8. README.md

This order is for making the code, not because Python runs the files in this exact order.

Start with `requirements.txt` because we need to decide what tools the project uses. For this project, we need FastAPI for the web API, scikit-learn for the trained model, pandas and NumPy for data preparation, and joblib for loading `.pkl` files.

Next, create `schema.py`. Before writing prediction logic, we should decide what the user is allowed to send. This file is like the form template for `/predict`.

Then create `features.py`. After we know the input shape, we can write the logic that changes raw user input into model-ready columns. This is where the Session 1 feature engineering is recreated.

After that, create `model.py`. This file loads the saved artifacts from Session 1: the trained model, the threshold, and the model column order.

Then create `main.py`. At this point, the pieces already exist, so `main.py` can connect them into API endpoints. It receives input, calls `features.py`, uses the loaded model, applies the threshold, and returns the prediction.

(OPTIONAL) Finally, create `Dockerfile` and `.dockerignore`. These are not part of the prediction logic. They are used to package the app for deployment.
In short:

```text
requirements.txt = choose the tools
schema.py        = define the input and output shape
features.py      = prepare raw input for the model
model.py         = load the saved model files from session 1
main.py          = connect everything into API endpoints
Dockerfile       = package the app for deployment
.dockerignore    = keep unnecessary files out of Docker
README.md        = explain the project(OPTIONAL)
```

## Runtime Flow
This is what happens when someone actually calls the API:

```text
User sends JSON
        ↓
schema.py checks the JSON
        ↓
main.py receives the checked data
        ↓
features.py creates the model-ready columns
        ↓
model.py provides the trained model and threshold
        ↓
main.py returns the prediction
```

Simple version:

```text
schema.py -> features.py -> model.py -> main.py response
```

## What Each Important File Does

### `main.py`
This file creates the web API.
It has two endpoints:

```text
GET /health
POST /predict
```

`/health` checks whether the API is alive.
`/predict` receives shopper data and returns the model prediction.

### `schema.py`
This file defines the shape of the input.
For example, it says that:

```text
ProductRelated should be a number
Month should be text
Weekend should be true or false
```

This helps FastAPI check the input before it reaches the model.

### `features.py`
This file prepares the data before prediction.
The model was not trained only on the raw dataset columns. During Session 1, we created extra columns such as:

```text
TotalDuration
TotalPages
ProductDurationPerPage
ProductPageRatio
MonthNum
IsHolidaySeason
log features
```

That same work must happen again during deployment. If we skip this step, the model may receive incomplete or wrong data.

So users only send simple raw data, and `features.py` automatically creates the extra columns.

### `model.py`

This file loads three important artifacts:

```text
artifacts/online_shoppers_model.pkl
artifacts/threshold.pkl
artifacts/model_columns.pkl
```

`online_shoppers_model.pkl` is the trained model.
`threshold.pkl` tells the API when to say "Will Purchase" or "Will Not Purchase".
`model_columns.pkl` stores the exact column order from training. This is important because the model expects the data in the same shape it saw during Session 1.

## Why `model_columns.pkl` Matters
Machine learning models are picky about column order.
If the model learned from columns like this:

```text
Administrative, ProductRelated, BounceRates, ...
```

we should send the columns back in the same order during deployment.
`model_columns.pkl` helps us avoid manually writing and maintaining that full list inside the deployment code.

Important note:

```text
model_columns.pkl stores the column names.
features.py still creates the column values.
```

So `model_columns.pkl` does not replace `features.py`. They work together.

## Setup
Check Python:

```powershell
python --version
```

This project is designed for Python 3.10 or newer. Python 3.11 is recommended.
Create a virtual environment:

```powershell
py -3.11 -m venv venv
```

If that command does not work, install Python 3.11 first from python install manager:

```text
https://www.python.org/downloads/
```
py install 3.11
then proceed with making the venv once more

Deleting old venv(if necessary):
rmdir /s /q venv
## Install Packages

```powershell
pip install -r requirements.txt
```
But sometimes, PowerShell may block venv activation. If that happens, you can use the venv Python directly.
Recommended command:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

This installs FastAPI, scikit-learn, pandas, NumPy, and other packages needed by the API.

## Run Locally
Use this command:

```powershell
uvicorn main:app --reload
===(or)===
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

If it works, you should see a message saying Uvicorn is running.
Open this URL in your browser:

```text
http://localhost:8000/docs
```

This opens Swagger UI, an automatic testing page created by FastAPI.

## Test the API
In Swagger UI:
1. Open `POST /predict`
2. Click `Try it out`
3. Use this example JSON
4. Click `Execute`

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

Example response:

```json
{
  "will_purchase": true,
  "prediction": 1,
  "prediction_label": "Will Purchase",
  "probability": 0.618,
  "threshold": 0.49
}
```

The exact probability may be different depending on the trained model.

## How to Read the Result

```text
will_purchase
```

`true` means the model predicts the visitor will purchase.
`false` means the model predicts the visitor will not purchase.

```text
probability
```

This is the model's estimated chance that the visitor will purchase.

```text
threshold
```

This is the cutoff from Session 1.
For example, if the threshold is `0.49`:

```text
probability >= 0.49 -> Will Purchase
probability < 0.49  -> Will Not Purchase
```

## Run with Docker -> won't run if files are saved in oneDrive
Docker is optional here, but it is useful for testing before actual deployment in HuggingFace(because HuggingFace utilizes Docker, and fixing things after uploading it can be quite a hassle).
If only local learning and not deployment, Docker is not required. Running with `uvicorn` is enough.

Without Docker, the API depends on whatever is installed on someone's laptop:

```text
Python version
scikit-learn version
FastAPI version
operating system setup
local virtual environment
```

This can cause problems. For example, a model trained with one scikit-learn version may fail when loaded with another scikit-learn version.
Docker helps by packaging the app together with its environment.

Think of Docker as a lunchbox for the app:

```text
It carries the code, the model files, and the exact Python packages together.
```

So the API can run more consistently on:

```text
your laptop
another participant's laptop
a server
Hugging Face Spaces
cloud deployment
```

Docker becomes useful when you want to share, deploy, or avoid "it works on my computer" problems.

Docker packages the API so it can run in a clean environment.
Build the image(Make sure docker desktop is installed):

```powershell
docker build -t shoppers-api .
```

Run the container:

```powershell
docker run -p 8000:8000 shoppers-api
```

Open:

```text
http://localhost:8000/docs
```

Use Docker if you want to test a deployment-like environment on your own computer.

## Deploy to Hugging Face Spaces
Hugging Face Spaces can host this API online.
Use these steps:

1. Go to `https://huggingface.co`
2. Create an account or log in
3. Click your profile picture
4. Choose `New Space`
5. Give the Space a name, for example `online-shoppers-api`
6. Choose `Docker` as the Space SDK
7. Create the Space
8. Upload all files from this folder

Make sure these files are uploaded:
```text
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
DO NOT UPLOAD VENV! 

After upload, Hugging Face will build the Docker image.
When the build is finished, open:

```text
https://your-space-url/docs
```
https://(USERNAME)-(SPACENAME).hf.space/docs

for testing purposes: 
https://potatott-test-deployment-online-shoppers-fastapi.hf.space/docs
https://potatott-test-deployment-online-shoppers-fastapi.hf.space/health
if both docs & health works, then deployment is successful

## =================================================================================================
## Common Problems
### PowerShell blocks activation

If this command fails:

```powershell
venv\Scripts\activate
```

use this instead:

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

You do not need to activate the venv if you call its Python directly.

### `ModuleNotFoundError`

This means a package is missing.

Run:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### `online_shoppers_model.pkl was not found`
The trained model file must be inside the `artifacts` folder.

### `model_columns.pkl was not found`
The column list file must be inside the `artifacts` folder.

Create it from Session 1 with:

```python
joblib.dump(num_cols + cat_cols, "model_columns.pkl")
```

### The API runs, but prediction feels strange
Check that the feature engineering in `features.py` matches Session 1.
For machine learning deployment, this is one of the most important rules:

```text
The data preparation during training and deployment must match.
```

## Session 1 to Session 2 Checklist
Before deployment, Session 1 should produce:

```text
online_shoppers_model.pkl
threshold.pkl
model_columns.pkl
```

Session 2 should contain:

```text
FastAPI code
feature engineering code
the three saved files from Session 1
requirements.txt
Dockerfile
```

## Final Mental Model
The model is the brain.
FastAPI is the front desk.
`features.py` is the translator that changes normal user input into the format the model understands.
`model_columns.pkl` is the checklist that keeps the translator's output in the correct order.
