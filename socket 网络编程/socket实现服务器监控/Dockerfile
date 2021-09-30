FROM python:3.8.5-slim
COPY listen_server.py /listen/listen_server.py
WORKDIR /listen
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get upgrade -yq && \
    apt-get install --no-install-recommends -yq gcc python-dev
RUN pip install -i https://pypi.doubanio.com/simple psutil
CMD ["python3", "listen_server.py"]