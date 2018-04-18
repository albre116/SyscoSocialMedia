FROM ufoym/deepo

ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH

RUN apt-get update -y && apt-get install -y python-pip python-dev gfortran python-numpy \
  build-essential cmake git unzip pkg-config libopenblas-dev liblapack-dev \
  libapr1 libapr1-dev libatlas-base-dev libatlas-dev apt-utils libxml2-dev

ENV LAPACK /usr/lib/liblapack.so
ENV ATLAS /usr/lib/libatlas.so
ENV BLAS /usr/lib/libblas.so

RUN mkdir -p $CONDA_DIR && \
    echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh && \
    apt-get update && \
    apt-get install -y wget git libhdf5-dev g++ graphviz && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh && \
    echo "c59b3dd3cad550ac7596e0d599b91e75d88826db132e4146030ef471bb434e9a *Miniconda3-4.2.12-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash /Miniconda3-4.2.12-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.2.12-Linux-x86_64.sh

ENV NB_USER root
ENV NB_UID 1000

RUN mkdir -p /src
# Python
ARG python_version=3.5
ENV PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.5/dist-packages/
RUN conda install -y python=${python_version}
RUN pip install --upgrade pip
RUN conda install Pillow scikit-learn notebook pandas matplotlib mkl nose pyyaml six h5py
RUN conda install pygpu
RUN conda install -c r r-essentials

# Gdal
RUN conda install gdal


RUN (cd /src && \
     git clone https://github.com/fchollet/keras.git && \
     cd /src/keras && \
     python setup.py install)
ENV PYTHONPATH='/src/:$PYTHONPATH'

ADD theanorc /home/keras/.theanorc

ENV GRANT_SUDO yes

COPY ./ini_files/freetds.conf /etc/freetds.conf
COPY ./ini_files/odbc.ini /etc/odbc.ini
COPY ./ini_files/odbcinst.ini /etc/odbcinst.ini
RUN mkdir /etc/freetds/ && cp /etc/freetds.conf /etc/freetds/

RUN apt-get -y update && apt-get install -y cron \
	&& apt-get install -y freetds-common freetds-bin freetds-dev \
	&& apt-get install -y libprotobuf-dev libprotoc-dev

RUN apt-get -y update && apt-get install -y python-dev libsasl2-dev gcc \
  sasl2-bin libsasl2-2 libsasl2-dev libsasl2-modules

RUN pip install git+https://github.com/cloudera/thrift_sasl
ENV PATH=/usr/local/bin/:$PATH

RUN rm /etc/odbc.ini
RUN apt-get -y update && apt-get -y install freetds-dev tdsodbc \
  unixodbc unixodbc-dev

ADD requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt
RUN conda install GDAL
RUN conda install libgdal
ENV PATH=$PATH:/opt/conda/bin/

# Install Rise
RUN conda install -c damianavila82 rise
#RUN jupyter-nbextension install rise --py --sys-prefix
#RUN jupyter-nbextension enable rise --py --sys-prefix
#RUN jupyter nbextension install --py hide_code
#RUN jupyter nbextension enable --py hide_code
#RUN jupyter serverextension enable --py hide_code
#RUN ipcluster nbextension enable --py hide_code

RUN conda install gcc_linux-64

RUN R -e "install.packages(c('data.table','dplyr','dygraphs','forecast',\
'glmnet','htmltools','htmlwidgets','jsonlite',\
'mgcv','quantreg','stats','xts','zoo', 'zipcode', 'stringr','feather','XML', 'httr', 'ISOweek','cobs'), \
repos='http://cran.us.r-project.org',dependencies=TRUE)"

RUN R -e "install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'devtools', 'poLCA', 'uuid', 'digest'), \
repos='http://cran.us.r-project.org',dependencies=TRUE)"

RUN R -e "install.packages(c('rzmq','repr','IRkernel','IRdisplay'), repos = 'http://irkernel.github.io/', type = 'source')"

RUN conda install -c r ipython-notebook r-irkernel
RUN conda clean -yt

# Install the Confluent OSS Platform, librdkafka and the confluent-kafka Python package
RUN apt-get autoclean && apt-get update
RUN apt-get install -y wget software-properties-common build-essential freetds-dev
RUN wget -qO - http://packages.confluent.io/deb/3.3/archive.key | apt-key add -
RUN add-apt-repository "deb [arch=amd64] http://packages.confluent.io/deb/3.3 stable main"
RUN apt-get update && apt-get install -y confluent-platform-2.11 librdkafka-dev
RUN pip install --upgrade pip && pip install confluent-kafka[avro]

# Install XGBoost library
RUN git clone --recursive https://github.com/dmlc/xgboost && \
    cd xgboost && \
    make -j4 && \
    cd python-package; python setup.py install
ENV PYTHONPATH='/src/:/usr/local/lib/python3.5/dist-packages/'
RUN echo "y\n" | add-apt-repository ppa:chronitis/jupyter && apt-get update && apt-get install -y ijulia ijavascript irkernel iruby ihaskell

# Install twitter libraries
ADD requirements2.txt /home/requirements2.txt
RUN pip install -r /home/requirements2.txt

WORKDIR /src
