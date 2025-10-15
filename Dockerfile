FROM python:3.14.0-slim

RUN apt-get update && apt-get install -y \
    build-essential curl cmake && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install -r ./requirements.txt

COPY ./.streamlit ./.streamlit
COPY ./src ./src

EXPOSE 8501

CMD ["python3","streamlit","run","src/Main.py"]