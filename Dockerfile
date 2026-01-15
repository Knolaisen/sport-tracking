FROM python:3.12-slim

WORKDIR /usr/src/app
COPY app.py .
COPY pyproject.toml .
COPY uv.lock .
COPY notebooks/ notebooks/
RUN pip install uv
RUN uv sync
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["uv", "run", "app.py"]