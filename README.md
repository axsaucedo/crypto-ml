# Industrial Machine Learning Pipelines: Crypto ML
This is the code for the Industrial Machine Learning 
pipelines at the PyCon SK (Bratislava) 2017.

The slides for the machine learning pycon conference can be found here: [https://github.com/axsauze/industrial-machine-learning](https://github.com/axsauze/industrial-machine-learning)

## Dev setup

In order to configure, you will need:
* Python 3.6
* RabbitMQ


To build the environment using conda:
```
conda env create -f crypto_ml.yml 
```

## Containerised setup

Make sure you have the following installations:
* Minikube
* kubectl

Start a minikube server:
```
minikube start
```


