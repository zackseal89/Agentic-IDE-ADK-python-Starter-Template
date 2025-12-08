# Code Execution in ADK Agents

ADK agents can leverage several code execution capabilities to perform calculations, data analysis, and other dynamic operations.

## Built-in Code Execution Tools

### 1. Gemini Code Execution
Execute code using Gemini models for:
- Mathematical calculations
- Data analysis
- Logic operations
- Script execution

### 2. GKE Code Executor
For production environments, use:
- Secure and scalable code execution in GKE
- Sandboxed environment for safety
- Better resource management

### 3. Database Tools
Execute SQL queries with:
- BigQuery
- BigTable
- Cloud Spanner

## Implementing Code Execution in Your Agent

You can implement code execution in your agents using custom tools:

```python
import subprocess
import tempfile
import os
from typing import Dict, Any

def execute_python_code(code: str) -> Dict[str, Any]:
    """Execute Python code in a safe environment and return results.
    
    Args:
        code: The Python code to execute
        
    Returns:
        Dictionary containing output or error message
    """
    # For security, in production use a more isolated environment
    # This is a simplified example for development purposes
    try:
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute the code and capture output
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=30  # 30-second timeout
        )
        
        # Clean up the temporary file
        os.remove(temp_file)
        
        return {
            "success": True,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        os.remove(temp_file)  # Clean up even if timeout occurs
        return {
            "success": False,
            "error": "Code execution timed out after 30 seconds",
            "output": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": None
        }

# Add to your agent
root_agent = Agent(
    name="code_execution_agent",
    model="gemini-2.0-flash",
    description="An agent that can execute Python code.",
    instruction="""You are an agent that can execute Python code. When users request calculations,
    data processing, or other tasks that require code execution, use the execute_python_code tool.
    
    Guidelines:
    - Only execute code that is safe and appropriate
    - Explain the purpose of the code before executing it
    - Format code properly before passing to the tool
    - Never execute code that could harm the system or access sensitive data
    """,
    tools=[execute_python_code],
)
```

## Security Considerations

### 1. Sandboxing
- Always run user-generated code in isolated environments
- Implement timeouts to prevent infinite loops
- Limit resource consumption (CPU, memory)

### 2. Safe Execution Practices
- Never execute code with elevated privileges
- Validate and sanitize inputs before execution
- Use allowlists for allowed operations when possible
- Implement proper error handling

### 3. Production Considerations
- Use the GKE Code Executor for production deployments
- Implement proper authentication and authorization
- Monitor code execution for potential abuse
- Log execution activities for security auditing

## Best Practices

1. **Start Simple**: For initial development, use simple code execution tools
2. **Secure Gradually**: Implement security measures as your agent matures
3. **Test Thoroughly**: Validate code execution with various inputs
4. **Monitor**: Keep track of execution patterns and potential issues
5. **Document**: Clearly document when and how code execution is used

## Limitations

- Code execution tools can pose security risks
- Resource consumption can be high with complex operations
- Some environments may restrict code execution
- Execution time should be limited to prevent long-running operations

## Alternative Approaches

For safer code execution, consider:
1. Using Google's built-in code execution tools rather than custom implementations
2. Implementing read-only operations where possible
3. Using specialized tools for specific tasks rather than general code execution
4. Using serverless functions or other isolated execution environments