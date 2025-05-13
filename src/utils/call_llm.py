import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


def call_llm(
    messages,
    # model: str = "deepseek/deepseek-chat:free"
    # model: str = "meta-llama/llama-4-maverick:free",
    model: str = "gpt-4o-2",
) -> str:
    """
    Calls the LLM with the given prompt and returns the response as a string.
    """
    # client = OpenAI(
    #     base_url="https://openrouter.ai/api/v1",
    #     api_key=os.getenv("OPENROUTER_API_KEY"),
    # )
    client = AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    )
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def main():
    output = call_llm(messages=[{"role": "user", "content": "Hello, world!"}])
    print("\nLLM Response:\n")
    print(output)


if __name__ == "__main__":
    main()
