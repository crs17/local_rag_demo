FROM python:3.12-alpine as app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

# Copy the project into the image
COPY . /app
WORKDIR /app

# Install dependencies
RUN uv sync

CMD ["uv", "run", "fastapi", "run", "app/main.py"]
