FROM python:3.12.12 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt

FROM python:3.12.12-slim
WORKDIR /app

# Install LaTeX (texlive) and dependencies for PDF generation
# Using texlive-latex-base for minimal installation
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv .venv/
COPY . .
CMD ["/app/.venv/bin/fastapi", "run"]
