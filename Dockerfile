# Base Python3 image.
FROM python:3

# Add NodeJS apt repository
RUN \
  echo "deb https://deb.nodesource.com/node_12.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -

# Install OS dependencies.
RUN apt-get update && apt-get install binutils libproj-dev gdal-bin netcat nodejs -y

# Install Python requirements.
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files.
RUN mkdir /code
RUN mkdir /code/static
WORKDIR /code
COPY . /code

# Run the Django server.
CMD if [ "${DEBUG}" = "True" ]; then bash run-dev.sh; else bash run.sh; fi
