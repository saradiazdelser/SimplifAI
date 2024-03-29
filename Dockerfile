FROM python:3.10.7

WORKDIR /workdir 

RUN pip install gradio==3.41.0
RUN pip install trulens_eval==0.18.2
RUN pip install evaluate==0.4.1
RUN pip install spacy==3.7.3
RUN pip install bert_score==0.3.13
RUN pip install trulens==0.13.4
RUN pip install scipy==1.12.0
RUN pip install text_generation
RUN pip uninstall -y llama-index-agent-openai llama-index-core llama-index-embeddings-openai llama-index-legacy llama-index-llms-openai llama-index-multi-modal-llms-openai llama-index-program-openai llama-index-question-gen-openai llama-index-readers-file
RUN pip install llama-index==0.9.11 --upgrade --no-cache-dir --force-reinstall
RUN pip install pydantic==1.10.14

RUN python -m spacy download en_core_web_sm

COPY . .

CMD python frontend.py
