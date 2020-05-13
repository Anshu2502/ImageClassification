FROM python:3
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY classify_image.py .
CMD ["python3","app.py"]
