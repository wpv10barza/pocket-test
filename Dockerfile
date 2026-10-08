FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY pack ./pack
RUN python pack/02_dataset/generate_semantic_dataset.py \
 && python -c "from app.indexer import SemanticIndex; i=SemanticIndex.load(); assert len(i.records)==360" \
 && useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)" || exit 1
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
