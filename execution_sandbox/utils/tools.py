"""
Mock implementation of various email, LLM, and web tools for testing and prototyping.
Note: These are placeholders and do not perform real operations.
"""

from typing import Any, Dict, List, Optional


def fetch_emails(query: str, max_results: Optional[int] = 10) -> List[Dict[str, Any]]:
    """
    Fetches multiple emails based on a given query.

    Parameters:
        query (str): Search query to filter emails, e.g., keywords or sender email.
        max_results (int, optional): Maximum number of results to fetch. Default is 10.

    Returns:
        List[Dict[str, Any]]: List of matching emails with the following keys:
            - email_id (str): Unique identifier of the email.
            - sender (str): Sender's email address.
            - subject (str): Subject line of the email.
            - body (str): Email content.
            - timestamp (str): Time received in ISO 8601 format.
    """
    if not query:
        raise ValueError("The query parameter cannot be empty.")

    mock_data = [
        {
            "email_id": f"email_{i}",
            "sender": f"sender{i}@example.com",
            "subject": f"Subject {i}: {query}",
            "body": f"This is the body of the email that matches the query '{query}'.",
            "timestamp": f"2023-10-01T0{i}:00:00Z",
        }
        for i in range(1, (max_results or 10) + 1)
    ]

    return mock_data


def generate_response(
    subject: str, body: str, sender: Optional[str] = None
) -> Dict[str, str]:
    """
    Generates a basic reply email given the original subject and body.

    Parameters:
        subject (str): Subject of the original email.
        body (str): Body of the original email.
        sender (str, optional): Original sender's address.

    Returns:
        Dict[str, str]: A dictionary containing:
            - subject (str): Reply subject line.
            - body (str): Suggested reply content.
    """
    return {
        "subject": f"Re: {subject}",
        "body": "Thank you for your message. Here's my response.",
    }


def send_mail(
    recipient: str,
    subject: str,
    body: str,
    in_reply_to: Optional[str] = None,
    thread_id: Optional[str] = None,
    attachments: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, str]:
    """
    Sends an email to the specified recipient.

    Parameters:
        recipient (str): Email address to send the message to.
        subject (str): Email subject.
        body (str): Email body.
        in_reply_to (str, optional): ID of the message being replied to.
        thread_id (str, optional): ID of the email thread.
        attachments (list of dict, optional): Attachments with filename and content_base64.

    Returns:
        Dict[str, str]: A dictionary containing:
            - status (str): Success or failure message.
            - message_id (str): ID of the sent message.
    """
    return {"status": "success", "message_id": "msg-67890"}


def llm_generation(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 512,
    system_prompt: Optional[str] = None,
) -> Dict[str, str]:
    """
    Generates text based on a prompt using a mock LLM.

    Parameters:
        prompt (str): Input to generate from.
        temperature (float): Randomness level.
        max_tokens (int): Max tokens to generate.
        system_prompt (str, optional): Context-setting message.

    Returns:
        Dict[str, str]: A dictionary containing:
            - completion (str): Generated response text.
    """
    return {"completion": "This is a generated response based on the prompt."}


def search_web(query: str, num_results: int = 10) -> List[Dict[str, str]]:
    """
    Performs a simulated web search.

    Parameters:
        query (str): Search query.
        num_results (int): Number of results to return.

    Returns:
        List[Dict[str, str]]: A list of search results with keys:
            - title (str): Title of the result.
            - snippet (str): Short summary.
            - url (str): Link to the result.
    """
    return [
        {
            "title": "Example Web Result",
            "snippet": "This is a summary of the web page.",
            "url": "https://example.com",
        }
    ] * num_results


def search_scholar(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """
    Performs a simulated academic article search.

    Parameters:
        query (str): Search query for scholarly content.
        num_results (int): Number of results to return.

    Returns:
        List[Dict[str, Any]]: A list of academic results with keys:
            - title (str): Title of the paper.
            - authors (List[str]): List of authors.
            - abstract (str): Summary of the paper.
            - publication_date (str): Date published.
            - url (str): Link to the paper.
    """
    return [
        {
            "title": "Example Academic Paper",
            "authors": ["Author A", "Author B"],
            "abstract": "This paper explores...",
            "publication_date": "2024-01-01",
            "url": "https://scholar.example.com/paper",
        }
    ] * num_results


def fetch_web(url: str, extract_text: bool = True) -> Dict[str, str]:
    """
    Simulates fetching a web page's content.

    Parameters:
        url (str): URL of the web page to fetch.
        extract_text (bool): Whether to extract readable text.

    Returns:
        Dict[str, str]: A dictionary containing:
            - html (str): Raw HTML content.
            - text (str): Extracted text content if requested.
    """
    return {
        "html": "<html><body>Example Page</body></html>",
        "text": "Example Page" if extract_text else "",
    }


def generate_email_content(
    content: str,
    tone: str = "professional",
    custom_prompt: Optional[str] = None,
    temperature: float = 0.7,
) -> Dict[str, str]:
    """
    Generates email subject and body using LLM based on provided content and parameters.

    Parameters:
        content (str): The main content or key points to include in the email.
        tone (str): The desired tone of the email (e.g., "professional", "casual", "formal").
        custom_prompt (str, optional): Additional custom instructions for the LLM.
        temperature (float): Controls randomness of output (0.0 = deterministic, 1.0 = creative).

    Returns:
        Dict[str, str]: A dictionary containing:
            - subject (str): The generated email subject line.
            - body (str): The generated email body content.
    """
    greeting = (
        "Hey"
        if tone == "casual"
        else "Dear friend"
        if tone == "professional"
        else "To whom it may concern"
    )

    sign_off = (
        "Cheers"
        if tone == "casual"
        else "Best regards"
        if tone == "professional"
        else "Sincerely"
    )

    subject_variants = [
        "Check out this amazing place I found!",
        "You won't believe what I discovered",
        "Must-visit destination alert",
        "Exciting place to share with you",
    ]
    selected_subject = subject_variants[
        int(temperature * len(subject_variants)) % len(subject_variants)
    ]

    return {
        "subject": selected_subject,
        "body": f"""{greeting}!

I wanted to share something exciting with you. I recently discovered this incredible place and I thought you'd be interested.

{content}

{custom_prompt if custom_prompt else ""}

{sign_off},
[Your name]""",
    }


def get_weather_info(location: str, units: str = "metric") -> Dict[str, Any]:
    """
    Retrieves current weather information for a specified location.

    Parameters:
        location (str): Name of the city or geographic coordinates (latitude,longitude).
        units (str, optional): Units for the temperature ('metric' or 'imperial'). Defaults to 'metric'.

    Returns:
        Dict[str, Any]: Current weather information including:
            - temperature (float): Current temperature in the specified units.
            - condition (str): Current weather condition (e.g., 'Sunny', 'Rain').
            - humidity (int): Humidity percentage.
            - wind_speed (float): Wind speed in the specified unit system.
    """
    if not location:
        raise ValueError("Location must be provided.")
    if units not in {"metric", "imperial"}:
        raise ValueError("Invalid units. Choose 'metric' or 'imperial'.")

    # Mock data based on sample parameters
    return {
        "temperature": 22.3 if units == "metric" else 72.1,
        "condition": "Cloudy",
        "humidity": 58,
        "wind_speed": 6.4 if units == "metric" else 3.98,
    }


def summarize_text(
    text: str, style: str = "neutral", length: str = "medium"
) -> Dict[str, str]:
    """
    Generates a summary of the given text with specified content style and length.

    Parameters:
        text (str): The input text to summarize.
        style (str, optional): The style of the summary (e.g., "formal", "casual", "neutral").
        length (str, optional): The desired length of the summary (e.g., "short", "medium", "long").

    Returns:
        Dict[str, str]: A dictionary containing:
            - summary (str): The summarized text.
            - style (str): The summary style.
            - length (str): The summary length.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")

    if style not in {"formal", "casual", "neutral"}:
        raise ValueError(
            f"Invalid style: {style}. Choose from 'formal', 'casual', or 'neutral'."
        )

    if length not in {"short", "medium", "long"}:
        raise ValueError(
            f"Invalid length: {length}. Choose from 'short', 'medium', or 'long'."
        )

    return {
        "summary": "This is a mock summary based on the requested style and length.",
        "style": style,
        "length": length,
    }


def search_datasets(research_topic: str, source: str = "all") -> List[Dict[str, Any]]:
    """
    Searches public repositories for datasets relevant to a research topic.

    Parameters:
        research_topic (str): The topic or keywords to search for.
        source (str, optional): The repository to search in (e.g., 'Kaggle', 'UCI', 'all'). Defaults to 'all'.

    Returns:
        List[Dict[str, Any]]: A list of datasets with keys:
            - name (str): The name of the dataset.
            - description (str): A brief description of the dataset.
            - source (str): The repository where the dataset is available.
            - url (str): The URL to access the dataset.
            - size (str): The size of the dataset (e.g., '10MB', '1GB').
    """
    if not research_topic:
        raise ValueError("The 'research_topic' parameter cannot be empty.")

    if source not in {"Kaggle", "UCI", "all"}:
        raise ValueError(
            "Invalid value for 'source'. Must be 'Kaggle', 'UCI', or 'all'."
        )

    # Mock data
    return [
        {
            "name": "Global Temperature Data",
            "description": "A dataset containing historical temperature data across the globe.",
            "source": "Kaggle",
            "url": "https://kaggle.com/datasets/global-temperature",
            "size": "20MB",
        },
        {
            "name": "Iris Dataset",
            "description": "A classic dataset for machine learning on iris plant classification.",
            "source": "UCI",
            "url": "https://archive.ics.uci.edu/ml/datasets/iris",
            "size": "10KB",
        },
    ]


def critique_paper(
    draft: str, reviewer_personas: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Provides critique or review suggestions for a draft paper using simulated reviewer personas.

    Parameters:
        draft (str): The draft paper text to critique.
        reviewer_personas (List[str], optional): List of reviewer personas, such as
            "Editor","Scientist", "General Reader", etc.

    Returns:
        List[Dict[str, Any]]: A list of critiques with keys:
            - persona (str): The reviewer persona providing the critique.
            - feedback (str): Specific feedback or suggestions for the draft.
            - strengths (List[str]): Identified strengths in the draft.
            - weaknesses (List[str]): Identified weaknesses in the draft.
    """
    # Mock implementation with example data
    return [
        {
            "persona": "Editor",
            "feedback": "The paper is well-structured, but the introduction lacks a clear thesis statement.",
            "strengths": ["Clear structure", "Good use of citations"],
            "weaknesses": ["Weak thesis statement", "Needs stronger conclusion"],
        },
        {
            "persona": "Scientist",
            "feedback": "The methodology is rigorous, but the discussion does not fully explore the implications of the results.",
            "strengths": ["Strong methodology", "Relevant references"],
            "weaknesses": ["Shallow discussion", "Some missing data points"],
        },
        {
            "persona": "General Reader",
            "feedback": "The paper is informative, but some technical terms are not explained, making it hard to follow.",
            "strengths": ["Interesting topic", "Engaging writing"],
            "weaknesses": [
                "Lack of non-technical explanations",
                "Jargon-heavy in some areas",
            ],
        },
    ]


def extract_structured_data(
    document_path: str, template: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Extracts structured data from semi-structured documents.

    Parameters:
        document_path (str): The file path to the semi-structured document to process.
        template (dict, optional): An optional template for extracting specific fields,
            e.g., {"name": "regex_for_name", "date": "regex_for_date"}.

    Returns:
        List[Dict[str, Any]]: A list of extracted data entries where each entry includes:
            - field_name (str): The name of the extracted field.
            - value (str): The extracted value for the field.
            - confidence (float): Confidence level of the extraction (0.0 to 1.0).
    """
    # Mock implementation with sample data
    if not document_path.endswith((".pdf", ".docx", ".txt")):
        raise ValueError(
            "Unsupported file format. Please provide a .pdf, .docx, or .txt file."
        )

    return [
        {"field_name": "Name", "value": "John Doe", "confidence": 0.95},
        {"field_name": "Date", "value": "2023-10-07", "confidence": 0.99},
        {"field_name": "Total Amount", "value": "$1,250.00", "confidence": 0.92},
    ]
