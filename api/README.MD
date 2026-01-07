python -m pip install --upgrade pip
pip install -r requirements.txt
# pip install fastapi uvicorn

python -m uvicorn main:app --host 0.0.0.0 --port 8000


# http://localhost:8000/cv