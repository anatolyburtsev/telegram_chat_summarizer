from typing import List

import tiktoken
from toolz import curry


@curry
def is_text_too_big(text, max_tokens=32000, model_name="gpt-4"):
    tokenizer = tiktoken.encoding_for_model(model_name)
    tokens = tokenizer.encode(text)
    return len(tokens) > max_tokens


def split_lines_into_chunks(lines: List[str], is_text_too_big) -> List[List[str]]:
    if is_text_too_big("".join(lines)):
        middle_index = len(lines) // 2
        part1 = lines[: int(1.1 * middle_index)]
        part2 = lines[int(0.9 * middle_index) :]

        return split_lines_into_chunks(
            part1, is_text_too_big
        ) + split_lines_into_chunks(part2, is_text_too_big)
    else:
        return [lines]


def split_file(file_path: str, max_tokens: int = 32000) -> List[List[str]]:
    is_text_too_big_curried = is_text_too_big(max_tokens=max_tokens, model_name="gpt-4")
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return split_lines_into_chunks(lines, is_text_too_big_curried)


def get_file_size_tokens(file_path, model_name="gpt-4"):
    tokenizer = tiktoken.encoding_for_model(model_name)

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        tokens = tokenizer.encode(content)
        return len(tokens)


if __name__ == "__main__":
    file_path = "chat_backup.txt"
    parts = split_file(file_path)
    print(f"{len(parts)}")
    for i in parts:
        print(f"{len(i)}")
