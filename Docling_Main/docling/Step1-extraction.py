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
conv_results_iter = converter.convert_all(sitemap_urls)

docs = []
for result in conv_results_iter:
    if result.document:
        document = result.document
        docs.append(document)