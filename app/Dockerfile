# FROM python:3.8-alpine
# WORKDIR /src
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY ./src /src
# EXPOSE 5000
# CMD python server.py

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update && apt-get install -y \
    wget \
	libopencv-dev \
        python3-pip \
	python3-opencv && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get install build-essential python3-dev

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

ADD requirements.txt .
RUN pip3 install -r requirements.txt

RUN conda update -n base -c defaults conda && \
    conda install jupyter -y && \
    conda install -c conda-forge opencv && \
    conda install numpy pandas scikit-learn matplotlib seaborn pyyaml h5py -y && \
    conda install -c https://conda.anaconda.org/conda-forge mahotas && \
    conda install scikit-image &&\ 
    conda install -c conda-forge xgboost && \
    pip3 install imutils 


RUN ["mkdir", "src"]

WORKDIR /src

COPY ./src /src

EXPOSE 5000


CMD python app.py