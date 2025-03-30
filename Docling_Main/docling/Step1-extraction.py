from docling.document_converter import DocumentConverter
from utils.sitemap import get_sitemap_urls

converter = DocumentConverter()

# --------------------------------------------------------------
# Basic PDF extraction
# Document 1
# Original Document - https://www.safetyforward.com/docs/legal.pdf
# Document 2
# https://www.apple.com/newsroom/pdfs/fy2024-q1/FY24_Q1_Consolidated_Financial_Statements.pdf
# This document is about not using mobile phones while driving a motor vehicle and prohibits disabling its motion restriction features.
# --------------------------------------------------------------

result = converter.convert("https://www.apple.com/newsroom/pdfs/fy2024-q1/FY24_Q1_Consolidated_Financial_Statements.pdf")

document = result.document
markdown_output = document.export_to_markdown()
json_output = document.export_to_dict()
print(markdown_output)

# --------------------------------------------------------------
# Basic Excel file  extraction
# Excel file 
# --------------------------------------------------------------
result = converter.convert("C:/Users/rajen/OneDrive/Documents/GitHub/RAG-Cookbook/Docling_Main/docling/uploaded_file.xlsx")

document = result.document
markdown_output = document.export_to_markdown()
json_output = document.export_to_dict()
print(markdown_output)

# --------------------------------------------------------------
# Basic HTML extraction
# --------------------------------------------------------------

result = converter.convert("https://python.langchain.com/docs/introduction/")

document = result.document
markdown_output = document.export_to_markdown()
print(markdown_output)

# --------------------------------------------------------------
# Scrape multiple pages using the sitemap
# --------------------------------------------------------------

sitemap_urls = get_sitemap_urls("https://www.langchain.com/")

# Print the sitemap URLs
print("\nSitemap URLs from https://www.langchain.com/:")
for i, url in enumerate(sitemap_urls, 1):
    print(f"{i}. {url}")
print(f"\nTotal URLs found: {len(sitemap_urls)}")

conv_results_iter = converter.convert_all(sitemap_urls)

docs = []
for result in conv_results_iter:
    if result.document:
        document = result.document
        docs.append(document)

# Print information about all collected documents
print("\nCollected Documents:")
for i, doc in enumerate(docs, 1):
    # Print document title or URL if available
    title = getattr(doc, 'title', None) or getattr(doc, 'url', f"Document {i}")
    print(f"\n{i}. {title}")
    
    # Print document content (markdown format)
    try:
        markdown = doc.export_to_markdown()
        # Print first 200 characters of content as preview
        preview = markdown[:200] + "..." if len(markdown) > 200 else markdown
        print(f"Preview: {preview}")
    except Exception as e:
        print(f"Could not export document to markdown: {e}")

print(f"\nTotal documents collected: {len(docs)}")
