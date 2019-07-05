## get python image
FROM python:3

## set up directory
WORKDIR /usr/src/app

## copy reqs
COPY requirements.txt ./

## install packages
RUN pip install --no-cache-dir -r requirements.txt

## copy all files into usr/src/app
COPY . . 


## Run command
CMD ["python", "app.py"]


### sudo docker-compose build
### sudo docker-compose up
