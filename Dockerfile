FROM python:3.13-slim

ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync

COPY ./src ./src
WORKDIR /app/src

# CMD [ "uv", "tree" ]

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
