from conda/miniconda3-centos7:latest

ADD ./crypto_ml /crypto_ml/
ADD ./crypto_ml.yml /crypto_ml/crypto_ml.yml
WORKDIR crypto_ml

RUN conda env create -f crypto_ml.yml
RUN yum install mesa-libGL -y
RUN mkdir /crypto_ml/logs/

