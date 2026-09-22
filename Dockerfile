FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
COPY knowledge ./knowledge
COPY schemas ./schemas
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -e .

EXPOSE 8080
CMD ["python", "-m", "kim_holiday.api", "--host", "0.0.0.0", "--port", "8080"]
