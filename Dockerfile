FROM python:3.11-slim

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    && sed -i 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# 4. Set up the working directory inside the container
WORKDIR /my_app


COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir uvicorn fastapi && \
    pip3 install --no-cache-dir -r requirements.txt


COPY ./my_app /my_app/my_app


CMD ["python3", "-m", "uvicorn", "my_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
