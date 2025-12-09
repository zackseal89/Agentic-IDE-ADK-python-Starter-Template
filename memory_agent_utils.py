"""
Utility script for initializing memory-enabled ADK agents.

This script helps set up the necessary configuration for agents 
that use the new context engineering capabilities.
"""

import os
import json
from pathlib import Path
import argparse


def create_memory_agent(agent_name: str, destination: str = "agents"):
    """
    Create a memory-enabled agent with all necessary files.
    
    Args:
        agent_name: Name of the agent to create
        destination: Directory where agent should be created
    """
    # Define source and destination paths
    source_dir = Path("templates/memory_agent")
    dest_dir = Path(destination) / agent_name
    
    # Verify source exists
    if not source_dir.exists():
        print(f"Error: Source directory {source_dir} does not exist")
        return False
    
    # Create destination directory
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files from template
    for file_path in source_dir.glob("*"):
        if file_path.is_file():
            dest_file = dest_dir / file_path.name
            dest_file.write_text(file_path.read_text())
    
    print(f"Memory-enabled agent '{agent_name}' created successfully at {dest_dir}")
    print("\nNext steps:")
    print(f"1. Update {dest_dir}/.env with your API keys")
    print(f"2. Review and customize {dest_dir}/agent.py")
    print(f"3. Test the agent: adk run {destination}/{agent_name}")
    
    return True


def setup_memory_storage_config(agent_path: str):
    """
    Create a configuration file for memory storage options.
    
    Args:
        agent_path: Path to the agent directory
    """
    config_content = {
        "memory_storage": {
            "vector_db": {
                "provider": "pinecone",  # Options: pinecone, weaviate, chromadb, or None
                "api_key_env_var": "VECTOR_DB_API_KEY",
                "environment": "us-west1-gcp",
                "timeout": 10
            },
            "knowledge_graph": {
                "provider": "neo4j",  # Options: neo4j, None
                "uri_env_var": "NEO4J_URI",
                "user_env_var": "NEO4J_USER",
                "password_env_var": "NEO4J_PASSWORD"
            }
        },
        "session_management": {
            "max_token_limit": 3000,
            "ttl_days": 7,
            "enable_pii_redaction": True
        },
        "memory_management": {
            "importance_threshold": 0.3,
            "max_memories_per_query": 5,
            "consolidation_interval_hours": 24
        }
    }
    
    config_path = Path(agent_path) / "memory_config.json"
    with open(config_path, 'w') as f:
        json.dump(config_content, f, indent=2)
    
    print(f"Memory configuration created at {config_path}")
    

def main():
    parser = argparse.ArgumentParser(description="Utility for memory-enabled ADK agents")
    parser.add_argument("command", choices=["create", "setup-config"], 
                       help="Command to execute")
    parser.add_argument("--name", help="Name of the agent (for create command)")
    parser.add_argument("--path", help="Path to agent directory (for setup-config command)")
    
    args = parser.parse_args()
    
    if args.command == "create":
        if not args.name:
            print("Error: --name is required for create command")
            return
        
        create_memory_agent(args.name)
        
    elif args.command == "setup-config":
        if not args.path:
            print("Error: --path is required for setup-config command")
            return
            
        setup_memory_storage_config(args.path)


if __name__ == "__main__":
    main()