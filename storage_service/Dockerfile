ARG PYTHON_IMAGE=python:3.12-slim

FROM ${PYTHON_IMAGE} AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --no-compile \
    --prefix=/install -r requirements.txt


FROM ${PYTHON_IMAGE} AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN useradd --create-home --uid 10001 app \
    && mkdir -p /data \
    && chown app:app /data

COPY --from=builder /install /usr/local

WORKDIR /app

COPY --chown=app:app app ./app

USER app

EXPOSE 8001

CMD ["python", "-m", "app.main"]
