ARG PYTHON_VERSION=3.11-slim

# COMPILER
FROM python:${PYTHON_VERSION} AS builder
ARG APP_VERSION

# install PDM
#RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY token_val/ /project/token_val/

# install dependencies and project into the local packages directory
WORKDIR /project

# 2 step pdm-sync and
RUN echo 'version="${APP_VERSION}"' > token_val/version.py
RUN mkdir __pypackages__ && pdm sync --prod --no-editable


# run stage
FROM python:${PYTHON_VERSION} as runner-base
ARG PYTHON_VERSION=3.11

RUN set -eux; \
	apt-get update; \
	apt-get install -y gosu tini; \
	rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 1500 token; \
    useradd --uid 1500 -g token -b /project -M -s /bin/sh token; \
    mkdir /keys; \
    mkdir /tokens;

WORKDIR /project
# retrieve packages from build stage
COPY --from=builder /project/__pypackages__/${PYTHON_VERSION}/lib /project/pkgs
COPY --from=builder /project/__pypackages__/${PYTHON_VERSION}/bin/* /bin/

ENV PYTHONPATH=/project/pkgs

COPY docker/entrypoint.sh /project/

ENV USER="1500:1500"

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["server"]
