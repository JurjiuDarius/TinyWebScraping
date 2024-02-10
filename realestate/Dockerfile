FROM selenium/standalone-chrome

WORKDIR /app

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["scrapy", "crawl", "apartments"]