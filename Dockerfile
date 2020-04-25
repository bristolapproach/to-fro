# Base Python3 image.
FROM python:3

# Install OS dependencies.
RUN apt-get update && apt-get install binutils libproj-dev gdal-bin netcat -y

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
