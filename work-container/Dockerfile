FROM ubuntu:latest
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:/opt/spark/bin:/opt/kafka/bin
RUN apt update -y && apt install -y openjdk-11-jdk wget
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc
RUN wget https://ftp.jaist.ac.jp/pub/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop3.2.tgz && tar zfx spark-3.0.0-bin-hadoop3.2.tgz
RUN mv spark-3.0.0-bin-hadoop3.2 /opt/spark
RUN wget https://ftp.kddi-research.jp/infosystems/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz && tar zfx kafka_2.13-2.6.0.tgz && mv kafka_2.13-2.6.0 /opt/kafka
RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean
RUN rm -f anaconda.sh spark-3.0.0-bin-hadoop3.2.tgz kafka_2.13-2.6.0.tgz

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]