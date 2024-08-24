from AI_app import OpenAIApp
import streamlit as st
import os
import fitz  # PyMuPDF


class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

    def __repr__(self):
        return (
            f"Document(page_content={self.page_content!r}, metadata={self.metadata!r})"
        )


def pdf_to_markdown_with_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    documents = []  # This will hold the Document objects

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        markdown_output = ""

        for block in blocks:
            if "lines" in block:  # Only interested in text blocks
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        if "Bold" in span["font"]:  # Check if the span is bold
                            markdown_output += f"**{text}**"
                        else:
                            markdown_output += text
                    markdown_output += "\n"  # Add a newline at the end of each line

                markdown_output += "\n"  # Add an extra newline for paragraph separation

        # Remove trailing whitespace and newlines from markdown_output
        markdown_output = markdown_output.rstrip()

        # Create a Document object for the current page
        metadata = {"source": pdf_path, "page": page_num + 1}
        documents.append(Document(markdown_output, metadata))

    doc.close()
    return documents


def save_uploaded_file(uploaded_file):
    # Save the uploaded file to a temporary location
    with open("files/" + uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name


def process_file_and_text(uploaded_file, user_text):
    st.write("Processing the file and text...")

    if uploaded_file is not None:
        # saved_path = save_uploaded_file(uploaded_file)
        pages = pdf_to_markdown_with_metadata(uploaded_file)
        # Call openai
        process_openai = OpenAIApp()
        openai_answer = process_openai.start_gpt_process(user_text, pages)
        st.write(f"Answer GPT: {openai_answer}")
    else:
        st.write("No file uploaded.")


def list_uploaded_files(upload_dir):
    # List all files in the upload directory
    files = [
        f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))
    ]
    return files


def remove_file(upload_dir, filename):
    # Remove the file from the directory
    file_path = os.path.join(upload_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success(f"File '{filename}' has been deleted.")
    else:
        st.error(f"File '{filename}' not found.")


# Streamlit application
st.title("Testing  prompts with  basic content")

st.markdown(
    """
### Steps to Run

1. **Select a file already uploaded or upload new one.**
2. **Think of a prompt**
3. **Submit and wait for GPT answer**


---

**IMPORTANT:** Make sure to include `{context}` in your prompt.

"""
)
upload_dir = "files/"

# Ensure the upload directory exists
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# Display existing files
uploaded_files = list_uploaded_files(upload_dir)
selected_file = None
print(uploaded_files)
if uploaded_files:
    selected_file = st.radio(
        "Select an existing file",
        options=uploaded_files,
        help="Only one file can be selected from the list.",
    )

    if selected_file:
        if st.button("Delete Selected File"):
            remove_file(upload_dir, selected_file)
            uploaded_files = list_uploaded_files(upload_dir)  # Refresh the list
            selected_file = None

# File uploader
uploaded_file = st.file_uploader("Or upload a new file", type=["txt", "csv", "pdf"])

if uploaded_file is not None:
    # Save the new file and set it as the selected file
    file_path = save_uploaded_file(uploaded_file)
    selected_file = os.path.basename(file_path)

# Text input
user_text = st.text_area("Enter your text here")

# Submit button
if st.button("Submit"):
    if selected_file and user_text:
        process_file_and_text(os.path.join(upload_dir, selected_file), user_text)
    else:
        st.warning("Please select a file and enter some text before submitting.")
