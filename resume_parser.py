from langchain_community.document_loaders import PyPDFLoader

def extract_resume_text(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return " ".join([p.page_content for p in pages])

