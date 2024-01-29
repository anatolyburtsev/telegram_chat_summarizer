import click
from dotenv import load_dotenv
from openai import OpenAI

from utils import split_file


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--max_tokens",
    default=32000,
    help="Maximum chunk size in tokens. Default is 32,000.",
)
@click.option("--output", default="output.txt", help="Output file for the results.")
def process_file(filename: str, max_tokens: int, output: str):
    chunks = split_file(filename, max_tokens)

    load_dotenv()
    client = OpenAI()

    with open(output, "w") as file:
        for idx, chunk in enumerate(chunks):
            try:
                print(f"Processing chunk: {idx}")
                print(f"chunk: {idx}", file=file)
                data = " ".join(chunk)
                result = answer_question(data, client)
                print(result, file=file)
            except Exception as e:
                print(f"Error processing chunk {idx}: {e}")


def answer_question(data: str, client: OpenAI):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": f"You are a travel assistant for a major worldwide tourism company. You have access to customers"
                f" chat of a given hotel. Here is the data: {data}",
            },
            {
                "role": "user",
                "content": "I'm going to travel to that hotel with my spouse and 3 yo kid. "
                "Find if any information is useful and nice to know for me. Ignore everything around WiFi, adult"
                "entertainments, such as alcohol, and people argues. Interested in facts and relevant opinions. Don't "
                "suggest any further actions, e.g. check directly with the hotel or families should enjoy "
                "stay there. Please, just do an analysis",
            },
        ],
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    process_file()
