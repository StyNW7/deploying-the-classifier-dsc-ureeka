Create Venv:
python -m venv venv

Activate Venv:
source venv/bin/activate

Install Dependencies:
pip install -r requirements.txt

Run FastAPI:
uvicorn main:app --reload

Docker Build:
docker build -t online-shoppers-api .

Docker Run Container:
docker run -p 8000:8000 online-shoppers-api