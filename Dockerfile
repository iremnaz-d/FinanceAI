
FROM python:3.12-slim

LABEL authors="irem naz"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/presentation/run_app.py", "--server.port=8501", "--server.address=0.0.0.0"]




