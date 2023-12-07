import os

def load_env_variables():
    os.environ['PROJECT_NUMBER'] = '713261100076'
    os.environ['TestVariable'] = 'Secret loading works'
    os.environ['ENDPOINT_ID'] = '3910824321534132224'
    os.environ['LOCATION'] = 'us-central1'
    os.environ['CREDENTIALS_JSON'] = load_credential_file("GUI/fine-acronym-407108-017b3c3578de.json")

def load_credential_file(filenmae):

    with open(filenmae) as f:
        data = f.read()

    return data