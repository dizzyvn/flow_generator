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
            - thread_id (str): Unique identifier of the email thread.
    """
    mock_data = [
        {
            "email_id": f"email_{i}",
            "sender": f"sender{i}@example.com",
            "subject": f"Subject {i}: {query}",
            "body": f"This is the body of the email that matches the query '{query}'.",
            "timestamp": f"2023-10-01T0{i}:00:00Z",
            "thread_id": f"thread_{i}",
        }
        for i in range(1, (max_results or 10) + 1)
    ]

    return mock_data


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


def forward_email(
    email_id: str,
    recipient: str,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    attachments: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, str]:
    """
    Mocks forwarding an email to a specified recipient.

    Parameters:
        email_id (str): ID of the email to forward.
        recipient (str): Email address of the new recipient.
        subject (str, optional): Custom subject line. Defaults to "Fwd: <original subject>".
        body (str, optional): Custom body. Defaults to "Forwarded message: <original body>".
        attachments (list of dict, optional): Mock attachments.

    Returns:
        Dict[str, str]: A dictionary containing:
            - status (str): "success" or "failure".
            - forwarded_message_id (str): Mock ID of the forwarded message.
            - original_email_id (str): ID of the original message.
            - recipient (str): The new recipient's email.
    """
    # Mock lookup of the original email
    original_email = {
        "email_id": email_id,
        "sender": "original.sender@example.com",
        "subject": "Original Subject",
        "body": "This is the original email body.",
        "timestamp": "2023-10-01T10:00:00Z",
    }

    # Default values if subject/body not provided
    fwd_subject = subject or f"Fwd: {original_email['subject']}"
    fwd_body = body or (
        f"---------- Forwarded message ----------\n"
        f"From: {original_email['sender']}\n"
        f"Date: {original_email['timestamp']}\n"
        f"Subject: {original_email['subject']}\n\n"
        f"{original_email['body']}"
    )

    return {
        "status": "success",
        "forwarded_message_id": "fwd-12345",
        "original_email_id": email_id,
        "recipient": recipient,
        "subject": fwd_subject,
        "body": fwd_body,
    }


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


def write_email(
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


def write_file(
    file_content: str, file_path: str, metadata: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    """
    Saves the given content to a specified file path with optional metadata.

    Parameters:
        file_content (str): The content to be saved in the file.
        file_path (str): The location where the file should be saved.
        metadata (dict, optional): Optional metadata such as author, description, or tags.

    Returns:
        Dict[str, str]: A confirmation of the save operation with:
            - status (str): Status of the operation ('success' or 'failure').
            - file_path (str): The path where the file was saved.
            - message (str): Additional information about the operation.
    """
    try:
        # Mock file write operation
        if not file_path or not file_content:
            raise ValueError("Invalid file path or content.")
        # Simulate saving the content (mock operation)
        return {
            "status": "success",
            "file_path": file_path,
            "message": "File saved successfully.",
        }
    except Exception as e:
        return {
            "status": "failure",
            "file_path": file_path,
            "message": f"An error occurred: {str(e)}",
        }


def read_file(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Reads the content of a file and retrieves metadata.

    Parameters:
        file_path (str): Path to the file to be read.
        encoding (str, optional): Encoding used to read the file. Defaults to 'utf-8'.

    Returns:
        Dict[str, Any]: File details and content including:
            - file_name (str): Name of the file.
            - file_size (int): Size of the file in bytes.
            - content (str): Content of the file.
            - lines (List[str]): List of lines in the file.
    """
    try:
        mock_file_size = 1024  # Mock size in bytes
        mock_content = "Mock file content line 1\nMock file content line 2"
        return {
            "file_name": file_path.split("/")[-1],
            "file_size": mock_file_size,
            "content": mock_content,
            "lines": mock_content.splitlines(),
        }
    except Exception as e:
        raise FileNotFoundError(f"Error accessing the file: {file_path}. Details: {e}")


def perform_deep_research(
    topic: str, level_of_research: str = "basic"
) -> Dict[str, Any]:
    """
    Conducts deep research on a given topic at the specified level of detail.

    Parameters:
        topic (str): The topic to be researched.
        level_of_research (str, optional): The depth of research required.
            Options are "basic", "intermediate", or "advanced". Defaults to "basic".

    Returns:
        Dict[str, Any]: Detailed research results including:
            - topic (str): The researched topic.
            - summary (str): Concise summary of the research.
            - key_points (List[str]): List of important findings.
            - sources (List[Dict[str, str]]): Reliable sources with:
                - source_name (str): Name of the source.
                - url (str): URL link to the source.
            - further_reading (List[str]): Recommendations for additional reading.
    """
    if not topic:
        raise ValueError("The 'topic' parameter cannot be empty.")

    mock_data = {
        "topic": topic,
        "summary": f"A brief overview of {topic}, emphasizing key aspects based on {level_of_research} research.",
        "key_points": [
            "Point 1: Significant finding related to the topic.",
            "Point 2: Another relevant observation.",
            "Point 3: Additional noteworthy detail.",
        ],
        "sources": [
            {"source_name": "Reliable Source A", "url": "https://example.com/source-a"},
            {
                "source_name": "Trusted Publication B",
                "url": "https://example.com/source-b",
            },
        ],
        "further_reading": [
            "Article: Deep Dive into the Subject",
            "Book: Comprehensive Guide to the Topic",
            "Research Paper: Evidence and Case Studies",
        ],
    }
    return mock_data


def retrieve_paper_pdf(
    paper_name: Optional[str] = None, url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves the PDF file of a research paper based on the given paper name or URL.

    Parameters:
        paper_name (str, optional): Name of the paper to retrieve.
        url (str, optional): URL of the paper to retrieve.

    Returns:
        Dict[str, Any]: Information about the retrieved paper including:
            - paper_name (str): Name of the paper.
            - url (str): URL of the paper.
            - pdf_link (str): Direct link to the PDF file.
            - status (str): Status of the retrieval process (e.g., 'success', 'not_found', 'error').
    """
    if not paper_name and not url:
        raise ValueError("Either 'paper_name' or 'url' must be provided.")

    # Mock logic and data
    if paper_name:
        return {
            "paper_name": paper_name,
            "url": f"https://example.com/{paper_name.replace(' ', '_')}",
            "pdf_link": f"https://example.com/{paper_name.replace(' ', '_')}.pdf",
            "status": "success",
        }
    elif url:
        return {
            "paper_name": "Example Paper",
            "url": url,
            "pdf_link": f"{url}/paper.pdf",
            "status": "success",
        }


def extract_text_from_document(file_path: str) -> str:
    """
    Extracts text content from a specified document.

    Parameters:
        file_path (str): Path to the document file.

    Returns:
        str: Extracted text content from the document.
    """
    try:
        # Mock implementation
        if file_path.endswith(".pdf"):
            return "This is a sample text extracted from a PDF document."
        elif file_path.endswith(".docx"):
            return "This is a sample text extracted from a DOCX document."
        elif file_path.endswith(".txt"):
            return "This is a sample text extracted from a TXT document."
        else:
            raise ValueError("Unsupported file type or file type not recognized.")
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from document: {e}")
