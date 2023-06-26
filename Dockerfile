FROM python:3.10-slim

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

CMD ["bash","start.sh"]
