# Kisan Sathi backend — works on Hugging Face Spaces (Docker) and Render.
FROM python:3.11-slim

WORKDIR /app

# Install CPU PyTorch first (smaller, no CUDA on free hosts), then the rest.
COPY requirements.txt .
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# App code
COPY app ./app
COPY data ./data

# Hugging Face Spaces expects port 7860; Render injects $PORT. Support both.
ENV PORT=7860
# Cache HF models in a writable dir inside the container.
ENV HF_HOME=/app/.hf_cache
EXPOSE 7860

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
