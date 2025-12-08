"""
Example deployment script for ADK agents to Vertex AI Agent Engine.

This script demonstrates how to prepare and deploy an ADK agent to Google's
managed Agent Engine service. Use this as a template for your own deployments.
"""

import vertexai
from vertexai import agent_engines


def deploy_agent(agent_path, project_id, location, display_name, staging_bucket=None):
    """
    Deploy an ADK agent to Vertex AI Agent Engine.

    Args:
        agent_path (str): Path to your agent directory
        project_id (str): Your Google Cloud Project ID
        location (str): Region for deployment (e.g., 'us-central1')
        display_name (str): Display name for your deployed agent
        staging_bucket (str, optional): GCS bucket for staging files
    """
    # Initialize the Vertex AI SDK
    if staging_bucket:
        vertexai.init(
            project=project_id,
            location=location,
            staging_bucket=staging_bucket,
        )
    else:
        # For Vertex AI Express mode
        vertexai.init(
            api_key="your-express-mode-api-key",  # Only if using Express mode
        )

    try:
        # Deploy the agent using the ADK CLI command
        import subprocess
        import sys
        
        cmd = [
            sys.executable, "-m", "google.adk.cli", "deploy", "agent_engine",
            "--project", project_id,
            "--region", location,
            "--display_name", display_name,
            agent_path
        ]
        
        if staging_bucket:
            cmd.extend(["--staging_bucket", staging_bucket])
            
        print(f"Deploying agent from {agent_path}...")
        print(f"Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Deployment successful!")
            print(result.stdout)
            return True
        else:
            print("Deployment failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False


def create_deployment_config():
    """
    Creates a sample configuration file for deployment.
    """
    config_content = """# Deployment Configuration for ADK Agent

# Google Cloud Project Configuration
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"  # Choose from supported regions
STAGING_BUCKET = "gs://your-gcs-bucket-name"  # Optional, for standard deployment

# Agent Configuration
AGENT_NAME = "my-agent"
AGENT_PATH = "./agents/my_agent"  # Path to your agent directory
DISPLAY_NAME = "My Production Agent"

# Deployment Mode
# Set to "express" for Vertex AI Express mode, "standard" for regular GCP project
DEPLOYMENT_MODE = "standard"
API_KEY = "your-api-key-here"  # Required only for express mode
"""
    
    with open("deployment_config.py", "w") as f:
        f.write(config_content)
    
    print("Sample deployment configuration created: deployment_config.py")
    print("Remember to update the values with your actual project details!")


# Example usage
if __name__ == "__main__":
    print("ADK Agent Deployment Helper")
    print("="*40)
    
    # Create a sample configuration file
    create_deployment_config()
    
    print("\nTo deploy your agent:")
    print("1. Update the deployment_config.py with your values")
    print("2. Ensure you have authenticated with Google Cloud:")
    print("   gcloud auth application-default login")
    print("3. Run this script or use the ADK CLI directly:")
    print("   adk deploy agent_engine --project=PROJECT_ID --region=REGION --display_name='Agent Name' /path/to/agent")