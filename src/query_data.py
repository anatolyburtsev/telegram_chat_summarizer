import click
from dotenv import load_dotenv
from openai import OpenAI

from utils import split_file


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--max_tokens', default=32000, help='Maximum chunk size in tokens. Default is 32,000.')
def process_file(filename: str, max_tokens: int):
    chunks = split_file(filename, max_tokens)

    load_dotenv()
    client = OpenAI()

    for idx, chunk in enumerate(chunks):
        print(f"Processing chunk: {idx}")
        data = ' '.join(chunk)
        result = answer_question(data, client)
        print(result)


def answer_question(data: str, client: OpenAI):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system",
             "content": f"You are a travel assistant for a major worldwide tourism company. You have access to customers"
                        f" chat of a given hotel. Here is the data: {data}"},
            {"role": "user", "content":
                "I'm going to travel to that hotel with my spouse and 3 yo kid. "
                "Find if any information is useful and nice to know for me. Ignore everything around adult"
                " entertainments, such as alcohol, and people argues. Interested in facts and relevant opinions. "}
        ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    process_file()
