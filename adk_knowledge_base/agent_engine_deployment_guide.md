# Deploying ADK Agents to Vertex AI Agent Engine

Agent Engine is a fully managed Google Cloud service enabling developers to deploy, manage, and scale AI agents in production. Agent Engine handles the infrastructure to scale agents in production so you can focus on creating intelligent and impactful applications.

## Preview: Vertex AI in express mode

If you don't have a Google Cloud project, you can try Agent Engine without cost using Vertex AI in Express mode.

---

## Prerequisites

You need the following resources configured to deploy to Agent Engine:

- Google Cloud account, with administrator access to:
  - Google Cloud Project: An empty Google Cloud project with billing enabled.
  - Python Environment: A Python version between 3.9 and 3.13.
  - UV Tool: Manage Python development environment and running Agent Starter Pack (ASP) tools.
  - Google Cloud CLI tool: The gcloud command line interface.
  - Make tool: Build automation tool.

For Vertex AI Express mode:
- API Key from Express Mode project: Sign up for an Express Mode project with your gmail account and get an API key.

## Standard Deployment Process

### 1. Set up Google Cloud Project

For Google Cloud Project:
1. Enable the Vertex AI API in your Google Cloud project
2. Authenticate with gcloud:
   ```
   gcloud auth application-default login
   ```
3. Create or use an existing Google Cloud Storage (GCS) bucket to stage your agent's code

For Vertex AI Express Mode:
1. Sign up for an Express Mode project and get an API key
2. No GCP project setup required

### 2. Install the required SDK

```
pip install google-cloud-aiplatform[adk,agent_engines]>=1.111
```

### 3. Prepare your agent for deployment

Create a `deploy.py` file with the following content:

For Google Cloud Project:
```python
import vertexai
from agent import root_agent # modify this if your agent is not in agent.py

# TODO: Fill in these values for your project
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"  # For other options, see supported regions
STAGING_BUCKET = "gs://your-gcs-bucket-name"

# Initialize the Vertex AI SDK
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

from vertexai import agent_engines

# Wrap the agent in an AdkApp object
app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)
```

For Vertex AI Express Mode:
```python
import vertexai
from agent import root_agent # modify this if your agent is not in agent.py

# TODO: Fill in these values for your api key
API_KEY = "your-express-mode-api-key"

# Initialize the Vertex AI SDK
vertexai.init(
    api_key=API_KEY,
)
```

### 4. Deploy your agent

You can deploy using either the ADK CLI or Python SDK.

**Using ADK CLI:**

For Google Cloud Project:
```
adk deploy agent_engine \
    --project=my-cloud-project-xxxxx \
    --region=us-central1 \
    --staging_bucket=gs://my-cloud-project-staging-bucket-name \
    --display_name="My Agent Name" \
    /my_agent_directory
```

For Vertex AI Express Mode:
```
adk deploy agent_engine \
    --display_name="My Agent Name" \
    --api_key=your-api-key-here
    /my_agent_directory
```

**Using Python SDK:**
```python
from vertexai import agent_engines

remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]"
    ]
)

print(f"Deployment finished!")
print(f"Resource Name: {remote_app.resource_name}")
```

The deployment process packages your code, builds it into a container, and deploys it to the managed Agent Engine service. This process can take several minutes.

## Accelerated Deployment with Agent Starter Pack (ASP)

This approach uses the ASP tool to provision a Google Cloud project with services needed for deploying your ADK project.

### Prepare your ADK project for ASP

1. Navigate to the parent directory that contains your agent folder
2. Run the ASP enhance command:
   ```
   uvx agent-starter-pack enhance --adk -d agent_engine
   ```
3. Follow the instructions from the ASP tool, accepting defaults and selecting a supported region

### Connect to your Google Cloud project

1. Login to your Google Cloud account:
   ```
   gcloud auth application-default login
   ```
2. Set your target project:
   ```
   gcloud config set project your-project-id-xxxxx
   ```
3. Verify your project:
   ```
   gcloud config get-value project
   ```

### Deploy your ADK project

1. Ensure you're in the parent directory containing your agent folder
2. Deploy using:
   ```
   make backend
   ```

## Testing your deployed agent

### Using Python SDK

Create a session and interact with your agent:
```python
from vertexai import agent_engines

# Get the deployed agent (if using CLI deployment)
# remote_app = agent_engines.get("your-agent-resource-name")

# Create a remote session
remote_session = await remote_app.async_create_session(user_id="u_456")
print(remote_session)

# Send queries to your remote agent
async for event in remote_app.async_stream_query(
    user_id="u_456",
    session_id=remote_session["id"],
    message="Your query here",
):
    print(event)
```

### Using REST calls

First, get your agent's query URL from the Google Cloud Console.

To create a session:
```
curl \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    https://$(LOCATION)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION)/reasoningEngines/$(RESOURCE_ID):query \
    -d '{"class_method": "async_create_session", "input": {"user_id": "u_123"},}'
```

To send a query:
```
curl \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://$(LOCATION)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION)/reasoningEngines/$(RESOURCE_ID):streamQuery?alt=sse -d '{
"class_method": "async_stream_query",
"input": {
    "user_id": "u_123",
    "session_id": "SESSION_ID_FROM_PREVIOUS_CALL",
    "message": "Your query here",
}
}'
```

## Deployment Payload

When you deploy your ADK agent project to Agent Engine, the following content is uploaded:
- Your ADK agent code
- Any dependencies declared in your ADK agent code

The deployment does not include the ADK API server or the ADK web user interface libraries. The Agent Engine service provides the libraries for ADK API server functionality.

## Clean up deployments

To delete your deployed agent and avoid charges:
```python
from vertexai import agent_engines

# Get your deployed agent
remote_app = agent_engines.get("your-agent-resource-name")

# Delete the deployed agent
remote_app.delete(force=True)
```

You can also delete your deployed agent via the Agent Engine UI on Google Cloud.