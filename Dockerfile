from conda/miniconda3-centos7:latest

ADD . /crypto_ml/
WORKDIR /crypto_ml/

RUN yum install mesa-libGL -y
RUN conda env create -f crypto_ml.yml

