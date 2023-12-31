# [Gradio](https://www.gradio.app/)
This documents contains relevant information to build the frontend by using Gradio. 

# With Vertex AI
Link to: [Google Documentation](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk)

Package that we need to connect to Vertex AI:
```
pip install google-cloud-aiplatform
```

How to Import the needed library:
```
from google.cloud import aiplatform
```

https://codelabs.developers.google.com/vertex-p2p-predictions#5

This is how to find the Project Number and ID and they are different: 
https://console.cloud.google.com/home


Fixed Credential Issue by:
copying the `fine-acronym-407108-017b3c3578de.json`
in the newly created
`mkdir ~/.config/gcloud`

To get the Service Account Credentials in:
https://www.youtube.com/watch?v=gywmAD3NRBo

Current Issue:
```
Unsupported region for Vertex AI, select from frozenset({'asia-east2', 'europe-southwest1', 'europe-west9', 'asia-northeast3', 'us-west2', 'asia-southeast1', 'me-west1', 'us-west4', 'asia-northeast1', 'australia-southeast1', 'us-east4', 'europe-west1', 'asia-south1', 'australia-southeast2', 'us-west3', 'us-west1', 'europe-west6', 'southamerica-west1', 'europe-west2', 'asia-east1', 'asia-northeast2', 'europe-west8', 'us-south1', 'southamerica-east1', 'us-central1', 'us-east1', 'europe-central2', 'europe-west4', 'asia-southeast2', 'northamerica-northeast2', 'europe-west3', 'europe-north1', 'northamerica-northeast1'})
```

## Connect to Endpoint
https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Endpoint


# Hosting 
For the [TruEra Challenge](https://lablab.ai/event/truera-challenge-build-llm-applications) that we build this application a domain to reach the application is part of the Submission so in this section there are ways to easy host a Gradio application. 

## Hugging Face Spaces
https://www.gradio.app/guides/sharing-your-app
-> use Hugging Face Spaces to share the App

- just have a GIT where you can commit to
- can use the online editor to edit Documents 

Just
- add requirements.txt
- just add the app.py to the repo and go
