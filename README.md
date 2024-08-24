# GPT Prompt Testing Application

This is a Streamlit application that allows you to test GPT prompts with basic content extracted from uploaded files. The app supports PDF, CSV, and text files, converting the content into markdown format and then using it as context for generating responses from the OpenAI GPT model.

## Features

- Upload and process PDF
- Convert PDF content to markdown format with metadata.
- Provide a prompt and get a GPT-generated response using the content from the uploaded file.
- Manage uploaded files: select, view, and delete them.

## Prerequisites

- Python 3.7 or higher
- Streamlit
- PyMuPDF (for PDF processing)
- LangChain (for GPT model chaining)
- OpenAI API Key (for accessing GPT models)
- dotenv (for managing environment variables)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/gpt-prompt-testing-app.git
   cd gpt-prompt-testing-app
   ```

2. Install the required packages:

   ```bash pip install -r requirements.txt

   ```

3. Set up the environment variables:

   ```bash OPENAI_KEY=your_openai_api_key_here

   ```

## Usage

1. Run the Streamlit application:

   ```bash streamlit run app.py

   ```

2. Follow the steps in the application:

   - Select a file: Choose an already uploaded file from the list or upload a new one.
   - Think of a prompt: Provide a custom prompt for the GPT model. Remember to include {context} in the prompt where you want the content to be injected.
   - Submit: Click the "Submit" button and wait for the GPT answer based on the provided context and prompt.

3. Manage files:

   - Delete: You can delete any previously uploaded files from the list if no longer needed.

## Important Notes

    - Make sure to include {context} in your prompt so that the content from the uploaded file can be properly injected.
    - The GPT model used is gpt-4o-2024-08-06. You can change the model version in the OpenAIApp class if needed.
