# set base image
FROM python:3.9

# set the working directory in the container
WORKDIR /app

# uncomment the following two lines to add the proxy settings when using Docker Desktop
#ENV http_proxy="http://host.docker.internal:3128"
#ENV https_proxy="http://host.docker.internal:3128"

# copy the dependencies file to the working directory
COPY requirements.txt ./

# install dependencies
RUN pip install -r requirements.txt
