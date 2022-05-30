FROM python:3.10.2-slim as dependencies

COPY install-poetry.py ./
RUN POETRY_HOME=/opt/poetry python install-poetry.py --yes
ENV PATH "/opt/poetry/bin:$PATH"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root

##################################
FROM python:3.10.2-slim as production

# postgres dependency - to see if needed or not
RUN apt update && apt --assume-yes install libpq5

COPY --from=dependencies /usr/src/app /usr/src/app

RUN useradd --uid 8001 --user-group --no-create-home app
RUN chown -R app:app /usr/src/app

USER app

ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/src/app

COPY dinopedia dinopedia
