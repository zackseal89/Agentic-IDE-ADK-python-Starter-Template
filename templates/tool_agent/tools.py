"""
Custom tools for the Tool Agent template.

Each tool is a Python function with:
- Type hints for all parameters and return values
- A descriptive docstring (CRITICAL - the LLM reads this!)
- Clear, structured return values
"""
from datetime import datetime
from typing import Optional


def get_current_time(city: str) -> dict:
    """Get the current time in a specified city.
    
    Use this when the user asks what time it is in a particular location.
    
    Args:
        city: The name of the city (e.g., "New York", "London", "Tokyo")
        
    Returns:
        Dictionary with:
        - city: The requested city name
        - time: Current time as a string
        - timezone: The timezone abbreviation
    """
    # This is a simplified example - in production, use a timezone library
    current_time = datetime.now().strftime("%I:%M %p")
    
    return {
        "city": city,
        "time": current_time,
        "timezone": "UTC",  # In reality, you'd calculate this based on city
    }


def search_items(query: str, category: Optional[str] = None, max_results: int = 5) -> dict:
    """Search for items in the catalog.
    
    Use this when the user wants to find products, items, or things
    by name, description, or category.
    
    Args:
        query: The search term (name, keyword, or description)
        category: Optional category to filter by (e.g., "electronics", "books")
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        Dictionary with:
        - query: The original search query
        - results: List of matching items with name, price, and description
        - total_count: Total number of matches found
    """
    # This is a mock implementation - replace with actual database/API calls
    mock_results = [
        {"name": f"Item matching '{query}'", "price": 29.99, "description": "A great product"},
        {"name": f"Another {query} item", "price": 49.99, "description": "Premium quality"},
    ]
    
    # Apply category filter if provided
    if category:
        mock_results = [r for r in mock_results if category.lower() in r["name"].lower()]
    
    # Limit results
    results = mock_results[:max_results]
    
    return {
        "query": query,
        "category": category,
        "results": results,
        "total_count": len(results),
    }
