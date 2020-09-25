FROM python:3.8-slim
WORKDIR api-smart-link
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential
RUN set -ex && pip3 install pip --upgrade
RUN pip install poetry
COPY pyproject.toml pyproject.toml
RUN poetry config virtualenvs.create false
COPY src src
COPY README.MD README.MD
COPY migrations.json migrations.json
EXPOSE 8788
RUN poetry install --no-dev
ENTRYPOINT ["poetry", "run", "api-smart-link-ctl"]
CMD ["server", "run"]
