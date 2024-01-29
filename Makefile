.PHONY: setup fetch_one_day fetch_week analyze

CHAT_NAME = solcaribebeach
DATE = $(shell date +%Y-%m-%d)

setup:
	@command -v poetry >/dev/null 2>&1 || { echo >&2 "Installing Poetry..."; pip install poetry; }
	@echo "Installing project dependencies..."
	@poetry install --no-root

fetch_one_day:
	@echo "Fetching data for one day..."
	@poetry run python src/fetch_data.py --chat_name $(CHAT_NAME) --days_back 1 --file_name chat_$(CHAT_NAME)_$(DATE).txt

fetch_week:
	@echo "Fetching data for one week..."
	@poetry run python src/fetch_data.py --chat_name $(CHAT_NAME) --days_back 7 --file_name chat_$(CHAT_NAME)_$(DATE).txt

analyze:
	@echo "Analyzing data..."
	@poetry run python src/query_data.py chat_$(CHAT_NAME)_$(DATE).txt --output analysis_$(CHAT_NAME)_$(DATE).txt

aggregate:
	@echo "Aggregating analysis data..."
	@poetry run python src/aggregate_analysis.py analysis_$(CHAT_NAME)_$(DATE).txt --output aggregated_$(CHAT_NAME)_$(DATE).txt
