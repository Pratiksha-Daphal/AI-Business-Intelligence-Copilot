# Gen AI BI Chatbot

This repository contains a chatbot application focused on business intelligence (BI) using generative AI.

## Overview

The project is designed to interpret natural language queries related to BI tasks, generate corresponding SQL queries, execute them against a database, and provide insights.

Key components include:

- **analytics/**: Core logic for query planning, SQL generation and validation, explanation, forecasting, and more.
- **api/**: FastAPI-based server to expose endpoints for query routing and processing.
- **data/**: Contains data files and documentation for datasets.
- **frontend/**: Application interface for users to interact with the chatbot.
- **llm/**: Language model utilities, prompts, and QA classes to handle natural language understanding.
- **memory/**: Conversation storage and summarization modules.
- **multimodal/**: Support for speech-to-text and other input modalities.

## Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API server**
   ```bash
   python api/main.py
   ```

3. **Launch the frontend**
   ```bash
   python frontend/app.py
   ```

## Testing

Unit tests are located under `analytics/test_nl_to_sql.py` and others may be added as the project evolves.

## Contributing

Feel free to open issues or pull requests to enhance functionality, improve documentation, or fix bugs.

## License

Specify license here if applicable.
