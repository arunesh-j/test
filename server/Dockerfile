FROM --platform=linux/amd64 python:3.11@sha256:eb79d3fc1b3d3991133634f12cb58c13e27a1abfe51f1c7ee03f6911bca5d412 as builder

# Installing browsers and utilities
RUN apt-get update && \
    apt-get install -y \
    chromium-driver ca-certificates curl jq wget git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/sh appuser
USER appuser
WORKDIR /server
RUN pip3 install --user pipenv setuptools wheel



ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV DD_TRACE_SAMPLING_RULES='[{"resource": "/healthz", "sample_rate": 0.0}]'
ENV DD_PATCH_MODULES="openai:false"

COPY --chown=appuser:appuser server/Pipfile* /server/

RUN pipenv requirements > requirements.txt
RUN pip install --user -r requirements.txt
RUN pip install --user pdfservices-sdk=="4.0.0" # Note: downgrade requests module
RUN pip install PyMuPDF=="1.24.5"

RUN python -m spacy download en_core_web_sm
COPY --chown=appuser:appuser server /server

# Compile Python files to bytecode
RUN python -m compileall -b /server

# Remove original .py files, excluding __init__.py files
RUN find /server -name "*.py" -not -name "__init__.py" -type f -delete

# Ensure the compiled files are executable
RUN chmod -R +x /server

CMD ["uvicorn", "app.main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8000", "--log-config" , "uvicorn_disable_logging.json"]