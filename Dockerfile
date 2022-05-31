FROM python:3.10.2-slim as dependencies

COPY install-poetry.py ./
RUN POETRY_HOME=/opt/poetry python install-poetry.py --yes
ENV PATH "/opt/poetry/bin:$PATH"

RUN mkdir -p /usr/dinopedia/app
WORKDIR /usr/dinopedia/app

RUN apt-get -yq update
RUN poetry config virtualenvs.in-project true

RUN apt-get --assume-yes install libpq-dev gcc

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root

##################################
FROM python:3.10.2-slim as production

# postgres dependency - to see if needed or not
RUN apt update && apt --assume-yes install libpq5

COPY --from=dependencies /usr/dinopedia/app /usr/dinopedia/app

RUN useradd --uid 8001 --user-group --no-create-home app
RUN chown -R app:app /usr/dinopedia/app

USER app

ENV VIRTUAL_ENV=/usr/dinopedia/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/dinopedia/app

COPY dinopedia dinopedia
