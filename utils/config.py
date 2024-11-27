import os

def load_config():
    """Load configuration from environment variables"""
    required_vars = [
        'OPENAI_API_KEY',
    ]
    
    # Check for required environment variables
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
    }
