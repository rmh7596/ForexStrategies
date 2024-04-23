#FROM registry.access.redhat.com/ubi9/python-39:1-117.1684741281
FROM python:3.11-alpine

COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

COPY . /app

ENTRYPOINT [ "python" ]

CMD ["ForexNewsScraper.py" ]