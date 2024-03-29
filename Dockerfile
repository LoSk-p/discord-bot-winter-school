FROM python:3.9
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY main.py main.py
COPY utils.py utils.py
COPY config/config.yaml config/config.yaml
CMD ["python3", "main.py"]