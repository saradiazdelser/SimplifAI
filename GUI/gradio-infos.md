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
