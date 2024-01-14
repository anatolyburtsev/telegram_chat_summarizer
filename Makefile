.PHONY: setup

CHAT_NAME = solcaribebeach

setup:
	@command -v poetry >/dev/null 2>&1 || { echo >&2 "Installing Poetry..."; pip install poetry; }
	@echo "Installing project dependencies..."
	@poetry install --no-root

fetch_one_day:
	@poetry run python src/fetch_data.py --chat_name $(CHAT_NAME) --days_back 1 --file_name chat_$(CHAT_NAME).txt

fetch_week:
	@poetry run python src/fetch_data.py --chat_name $(CHAT_NAME) --days_back 7 --file_name chat_$(CHAT_NAME).txt

analyze:
	@poetry run python src/query_data.py chat_$(CHAT_NAME).txt
