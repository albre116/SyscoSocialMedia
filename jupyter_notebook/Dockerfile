FROM python:3.6.4
RUN mkdir -p /usr/src/app
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y freetds-dev libgdal-dev libevent-dev python-dev build-essential \
libgdal-dev python-gdal
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')
RUN pip install shapely --no-binary shapely

# Install twitter libraries
COPY requirements.txt .
COPY requirements2.txt .
RUN pip install -r requirements.txt
RUN pip install -r requirements2.txt
RUN pip install git+git://github.com/albre116/visJS2jupyter
CMD /usr/local/bin/jupyter notebook --port=8888 --ip=0.0.0.0 --NotebookApp.password="sha1:f217aa434731:b01a46c5ffccfc413ccffc33c802882737ac2ccd" --allow-root
