"""
Code Execution Agent Template - An ADK agent with code execution capabilities.

This template demonstrates how to create an agent that can execute code safely.
It includes basic security measures and follows ADK best practices.
"""
from google.adk.agents.llm_agent import Agent
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
    # For security, use a timeout and limit resources
    # This is a simplified example - in production, use more robust isolation
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
            timeout=10  # 10-second timeout for safety
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
            "error": "Code execution timed out after 10 seconds",
            "output": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": None
        }


def calculate_expression(expression: str) -> Dict[str, Any]:
    """Safely evaluate a mathematical expression.
    
    Args:
        expression: The mathematical expression to evaluate
        
    Returns:
        Dictionary containing the result of the calculation
    """
    # For safety, use eval in a restricted environment
    # Only allow safe mathematical operations
    try:
        # Create a safe namespace with only math functions
        import math
        safe_dict = {
            "abs": abs, "round": round, "min": min, "max": max,
            "pow": pow, "sum": sum, "len": len, "math": math,
            "__builtins__": {},
            "x": eval(expression, {"__builtins__": {}}) if all(c in "0123456789+-*/(). " for c in expression) else None
        }
        
        # Validate expression contains only allowed characters
        if not all(c in "0123456789+-*/().% " for c in expression):
            return {"success": False, "error": "Invalid characters in expression", "result": None}
        
        result = eval(expression, safe_dict)
        return {
            "success": True,
            "result": result,
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "result": None
        }


root_agent = Agent(
    name="code_execution_agent",
    model="gemini-2.0-flash",
    description="An agent that can execute Python code and perform calculations.",
    instruction="""You are a helpful assistant with code execution capabilities.

Available tools:
- execute_python_code: Execute Python code in a safe environment
- calculate_expression: Safely evaluate mathematical expressions

Guidelines:
- Only execute code that is safe and appropriate
- Explain the purpose of the code before executing it
- Format code properly before passing to the tool
- Never execute code that could harm the system or access sensitive data
- For mathematical calculations, prefer the calculate_expression tool
- Respect timeout limits on code execution
""",
    tools=[execute_python_code, calculate_expression],
)