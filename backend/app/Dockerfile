FROM python:3.10

WORKDIR /opt/jodal

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["tail", "-f", "requirements.txt"]
