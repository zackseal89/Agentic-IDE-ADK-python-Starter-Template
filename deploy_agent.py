"""
Deploy script for ADK agents to Vertex AI Agent Engine.

This script handles the deployment of your ADK agent to Google's
managed Agent Engine service with proper configuration and error handling.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Deploy ADK agent to Vertex AI Agent Engine")
    parser.add_argument("--agent-path", required=True, help="Path to your agent directory")
    parser.add_argument("--project", required=True, help="Google Cloud Project ID")
    parser.add_argument("--region", default="us-central1", help="Region for deployment (default: us-central1)")
    parser.add_argument("--display-name", required=True, help="Display name for your deployed agent")
    parser.add_argument("--staging-bucket", help="GCS bucket for staging files (optional)")
    parser.add_argument("--api-key", help="API key for Vertex AI Express mode (optional)")
    
    args = parser.parse_args()
    
    # Validate agent path exists
    agent_path = Path(args.agent_path)
    if not agent_path.exists():
        print(f"Error: Agent path {args.agent_path} does not exist!")
        sys.exit(1)
    
    # Validate that the agent directory contains the expected files
    if not (agent_path / "agent.py").exists():
        print(f"Error: {args.agent_path} does not appear to be a valid ADK agent directory (missing agent.py)")
        sys.exit(1)
    
    # Construct the deployment command
    cmd = [
        sys.executable, "-m", "google.adk.cli", "deploy", "agent_engine",
        "--project", args.project,
        "--region", args.region,
        "--display_name", args.display_name,
        str(agent_path)
    ]
    
    if args.staging_bucket:
        cmd.extend(["--staging_bucket", args.staging_bucket])
    
    if args.api_key:
        cmd.extend(["--api_key", args.api_key])
    
    print(f"Deploying agent from {args.agent_path} to Agent Engine...")
    print(f"Project: {args.project}")
    print(f"Region: {args.region}")
    print(f"Display Name: {args.display_name}")
    
    if args.staging_bucket:
        print(f"Staging Bucket: {args.staging_bucket}")
    
    if args.api_key:
        print("Deployment Mode: Express (using API key)")
    else:
        print("Deployment Mode: Standard (using gcloud auth)")
    
    print("\nExecuting command:")
    print(" ".join(cmd))
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\n✅ Deployment successful!")
            print(result.stdout)
            return True
        else:
            print("\n❌ Deployment failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except FileNotFoundError:
        print("\n❌ Error: ADK CLI not found. Please ensure google-adk is installed.")
        print("You may need to run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Error during deployment: {e}")
        return False


if __name__ == "__main__":
    main()