FROM python:3

WORKDIR /opt/jodal

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD ["tail", "-f", "requirements.txt"]
