FROM python:3.10.7

WORKDIR /workdir 

RUN pip install gradio==3.41.0
RUN pip install trulens_eval==0.18.2
RUN pip install llama_index==0.9.11
RUN pip install evaluate==0.4.1
RUN pip install spacy==3.7.3
RUN pip install bert_score==0.3.13
RUN pip install trulens==0.13.4
RUN pip install scipy==1.12.0
RUN pip install text_generation

RUN python -m spacy download en_core_web_sm

COPY . .

CMD python frontend.py
