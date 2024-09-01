FROM python:3.11.2

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app/

WORKDIR /app/WNBA_scraper/WNBA_scraper

CMD ["scrapy", "crawl", "ballspider"]
# CMD ["python", "test.py"]
