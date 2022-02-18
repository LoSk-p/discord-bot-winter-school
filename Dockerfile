FROM python:3.6
RUN pip3 install -r requirements.txt
COPY main.py main.py
CMD ["python3", "plug.py"]