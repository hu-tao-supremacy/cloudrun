FROM continuumio/miniconda3:latest
WORKDIR /app
ENV PYTHONUNBUFFERED True
RUN conda install sqlalchemy flask psycopg2 -y
RUN conda install -c conda-forge sentence-transformers unzip -y
ADD https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/stsb-roberta-large.zip stsb-roberta-large-model.zip
RUN unzip stsb-roberta-large-model.zip -d ./src/stsb-roberta-large-model && rm stsb-roberta-large-model.zip
COPY . /app
CMD python ./src/main.py
