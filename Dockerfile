FROM python:3.10

# Configure poetry
ENV POETRY_VERSION=1.3.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Setup workdirectory
WORKDIR /user_api

COPY . .
RUN poetry install
CMD ["poetry", "run", "uvicorn", "--port", "5050", "--host", "0.0.0.0", "user_api.server:app"]

