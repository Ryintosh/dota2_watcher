#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="ryintosh"

WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY main.py ./
COPY modules/ ./modules/
COPY requirements.txt ./
COPY images/ ./images/
COPY fonts/ ./fonts/

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py"]