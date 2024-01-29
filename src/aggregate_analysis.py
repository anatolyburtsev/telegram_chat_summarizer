import click
from dotenv import load_dotenv
from openai import OpenAI


def read_input_file(filename):
    with open(filename, "r") as file:
        return file.read()


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--output", default="output.txt", help="Output file for the results.")
def process_file(filename: str, output: str):
    data = read_input_file(filename)

    load_dotenv()
    client = OpenAI()

    try:
        print("Processing file...")
        aggregated_data = aggregate_data(data, client)
        with open(output, "w") as file:
            print(aggregated_data, file=file)
        print(aggregated_data)
    except Exception as e:
        print(f"Error processing file: {e}")


def aggregate_data(data: str, client: OpenAI):
    prompt = f"Please aggregate the following information, remove any duplicates, and summarize it in a clear and concise manner:\n\n{data}"

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": "Please provide the aggregated summary.",
            },
        ],
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    process_file()
