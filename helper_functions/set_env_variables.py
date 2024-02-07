import os

def load_env_variables():

    #Set the Model Type
    os.environ['ModelType'] = "CTC_Madrid"

    #Env for VertexAI
    os.environ['PROJECT_NUMBER'] = '993668300869'
    os.environ['TestVariable'] = 'Secret loading works'
    os.environ['ENDPOINT_ID'] = '3910824321534132224'
    os.environ['LOCATION'] = 'us-central1'
    #os.environ['CREDENTIALS_JSON'] = load_credential_file("/Users/hpe/Programming/SimplifAI/GUI-Tests/igneous-visitor-407107-17758a215e3e.json")
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
    os.environ["OPENAI_API_KEY"] = ''
    
    #Env for Ollama
    

def load_credential_file(filenmae):

    with open(filenmae) as f:
        data = f.read()

    return data