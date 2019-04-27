FROM python:alpine3.6
ADD . /code
WORKDIR /code
EXPOSE 8000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD python app.py
