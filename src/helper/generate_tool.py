import argparse

from utils.call_llm import call_llm


def generate_tool_implementation(description: str) -> str:
    """
    Generate a Python function implementation based on a tool description.

    Args:
        description (str): Description of the tool to implement

    Returns:
        str: Generated Python function code
    """
    prompt = f"""Given the following tool description, generate a Python function implementation with:
1. Proper type hints
2. Comprehensive docstring with Parameters and Returns sections
3. Mock data that makes sense for the tool's purpose
4. Appropriate error handling

Here are some examples of good tool implementations:

Example 1 - Email Reading Tool:
def read_mail(
    email_account: str, 
    password_or_token: str, 
    filters: Optional[Dict] = None
) -> List[Dict[str, Any]]:
    \"\"\"
    Retrieves emails from the specified account with optional filters.

    Parameters:
        email_account (str): Email address to access.
        password_or_token (str): Authentication credential.
        filters (dict, optional): Optional filters such as unread_only, from_address, subject_keywords.

    Returns:
        List[Dict[str, Any]]: List of emails with keys:
            - email_id (str): Unique identifier of the email.
            - sender (str): Sender's email address.
            - subject (str): Subject line of the email.
            - body (str): Email content.
            - timestamp (str): Time received in ISO 8601 format.
            - thread_id (str): ID of the email thread if available.
    \"\"\"
    return [
        {{
            "email_id": "12345",
            "sender": "example@example.com",
            "subject": "Test Email",
            "body": "This is a test email.",
            "timestamp": "2025-05-13T12:00:00Z",
            "thread_id": "thread-001",
        }}
    ]

Example 2 - Weather API Tool:
def get_weather(
    location: str,
    units: str = "metric",
    forecast_days: int = 1
) -> Dict[str, Any]:
    \"\"\"
    Retrieves weather information for a specified location.

    Parameters:
        location (str): City name or coordinates.
        units (str, optional): Units of measurement ('metric' or 'imperial').
        forecast_days (int, optional): Number of days to forecast.

    Returns:
        Dict[str, Any]: Weather information including:
            - temperature (float): Current temperature
            - condition (str): Weather condition
            - humidity (int): Humidity percentage
            - wind_speed (float): Wind speed
            - forecast (List[Dict]): Daily forecast data
    \"\"\"
    return {{
        "temperature": 22.5,
        "condition": "Sunny",
        "humidity": 65,
        "wind_speed": 5.2,
        "forecast": [
            {{
                "date": "2024-03-14",
                "max_temp": 24.0,
                "min_temp": 18.0,
                "condition": "Partly Cloudy"
            }}
        ]
    }}

Now, please generate a similar implementation for this tool description:

{description}

The function should follow this template:
def tool_name(param1: type1, param2: type2 = None) -> return_type:
    \"\"\"
    Description of what the tool does.

    Parameters:
        param1 (type1): Description of param1
        param2 (type2, optional): Description of param2

    Returns:
        return_type: Description of what is returned
    \"\"\"
    # Implementation with mock data
    return mock_data

Only return the function code, no explanations or additional text."""

    response = call_llm(messages=[{"role": "user", "content": prompt}])
    return response


def main():
    parser = argparse.ArgumentParser(
        description="Generate a mock tool implementation from a description"
    )
    parser.add_argument("--description", help="Description of the tool to implement")

    args = parser.parse_args()

    implementation = generate_tool_implementation(args.description)
    implementation.replace("```python", "").replace("```", "")

    print(implementation)


if __name__ == "__main__":
    main()
