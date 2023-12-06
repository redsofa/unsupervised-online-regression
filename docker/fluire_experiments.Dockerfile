ARG FROM_SRC=amd64/ubuntu:22.04

FROM ${FROM_SRC}

ENV MINICONDA_SRC https://repo.anaconda.com/miniconda/Miniconda3-py310_23.9.0-0-Linux-x86_64.sh
ENV USER exp_user
ENV CONDA_DIR /home/$USER/apps/miniconda
ENV ROOT_PWD exp_user
ENV PATH=$CONDA_DIR/bin:$PATH

# # -- Layer: OS 
RUN apt update && \
    apt install -y wget && \
    apt install -y curl && \
    apt install -y gcc && \
    apt install -y cmake && \
    apt install -y make && \
    apt install -y bzip2 && \
    apt install -y unzip

# -- Layer : User
RUN echo "root:$ROOT_PWD" | chpasswd && \
    useradd -ms /bin/bash $USER

# -- Switch to $USER user
USER $USER

WORKDIR /home/$USER

# -- Layer : Conda
RUN mkdir /home/$USER/apps && \
    wget --quiet $MINICONDA_SRC -O miniconda.sh && \
    chmod +x miniconda.sh && \
    bash miniconda.sh -b -p $CONDA_DIR && \
    rm miniconda.sh && \
    conda init bash && \
    echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile && \
    echo "export PATH=$CONDA_DIR/bin:$PATH" >> $HOME/.bashrc && \
    echo "conda activate base" >> $HOME/.bashrc

# -- Layer : Python Packages
RUN conda update --name base --channel defaults conda && \
    conda install -y python=3.10 && \
    conda install -y scikit-learn=1.3.0 && \
    conda install -y matplotlib=3.7.2 && \
    conda install -y pandas=2.0.3 && \
    conda install -y conda-build=3.27.0 && \
    conda install -y pip && \
    pip install --upgrade pip && \
    pip install river==0.18.0 && \
    pip install numpy==1.25.2

# -- Layer : src and data files
RUN mkdir -p /home/$USER/src/bash
RUN mkdir -p /home/$USER/src/python
RUN mkdir -p /home/$USER/data/usup_reg

COPY ./src/bash /home/$USER/src/bash
COPY ./src/python /home/$USER/src/python
RUN conda develop /home/$USER/src/python/packages/fluire

# Reference : https://chemicloud.com/blog/download-google-drive-files-using-wget/
ENV RAW_FILE_ID 196XqrFcromdRgHeB5oQj2jRwo3FlrMJX
RUN wget --no-check-certificate "https://docs.google.com/uc?export=download&id=$RAW_FILE_ID" -O /home/$USER/data/raw.zip
RUN unzip /home/$USER/data/raw.zip -d /home/$USER/data/usup_reg
RUN rm -f /home/$USER/data/raw.zip

ENV WORK_FILE_ID 13-fB9jYBNpmTGwbqaQCqBIf6w6Y0aCUl
RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate https://docs.google.com/uc?export=download&id=$WORK_FILE_ID -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$WORK_FILE_ID" -O /home/$USER/data/work.zip && rm -rf /tmp/cookies.txt
RUN unzip /home/$USER/data/work -d /home/$USER/data/usup_reg
RUN rm -f /home/$USER/data/work.zip

# -- Runtime
CMD ["bash"]
