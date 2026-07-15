# syntax=docker/dockerfile:1
# The Python index digest supports linux/amd64 and linux/arm64. The concrete
# platform manifest selected by BuildKit is retained in Docker provenance.
FROM python:3.11-slim-bookworm@sha256:b18992999dbe963a45a8a4da40ac2b1975be1a776d939d098c647482bcad5cba

ARG CANDIDATE_SHA
ARG TDE_VERSION
ARG WHEEL_FILE
ARG WHEEL_SHA256
ARG SOURCE_DATE_EPOCH
ARG CREATED

LABEL org.opencontainers.image.title="Technical Debt Engine" \
      org.opencontainers.image.description="Canonical Engineering Runtime for technical debt analysis, qualification and reporting." \
      org.opencontainers.image.source="https://github.com/pcvantol/technical-debt-engine" \
      org.opencontainers.image.url="https://github.com/pcvantol/technical-debt-engine" \
      org.opencontainers.image.revision="${CANDIDATE_SHA}" \
      org.opencontainers.image.version="${TDE_VERSION}" \
      org.opencontainers.image.created="${CREATED}" \
      org.opencontainers.image.licenses="NOASSERTION"

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TDE_REPOSITORY=/workspace/repository \
    TDE_EVIDENCE_STORE=/workspace/evidence

# cloc 2.10 is a standalone Perl program; Radon is pinned to the qualified
# Python analyzer version. Neither is downloaded at container startup.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends ca-certificates perl \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir radon==6.0.1 \
    && python -c "import urllib.request; urllib.request.urlretrieve('https://github.com/AlDanial/cloc/releases/download/v2.10/cloc-2.10.pl', '/usr/local/bin/cloc')" \
    && echo 'bf59272455172108072a0a106379f7509fd4349bdcfd85203bac038ccd286d83  /usr/local/bin/cloc' | sha256sum --check \
    && chmod 0755 /usr/local/bin/cloc \
    && cloc --version | grep -Fx '2.10' \
    && radon --version | grep -F '6.0.1'

COPY wheel/${WHEEL_FILE} /tmp/${WHEEL_FILE}
RUN echo "${WHEEL_SHA256}  /tmp/${WHEEL_FILE}" | sha256sum --check \
    && python -m pip install --no-cache-dir --no-deps /tmp/${WHEEL_FILE} \
    && rm /tmp/${WHEEL_FILE} \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin tde \
    && mkdir -p /workspace/repository /workspace/evidence /workspace/config \
    && chown -R tde:tde /workspace

USER tde
WORKDIR /workspace/repository
VOLUME ["/workspace/repository", "/workspace/evidence", "/workspace/config"]
ENTRYPOINT ["tde"]
CMD ["--help"]
