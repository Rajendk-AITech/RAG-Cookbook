from typing import List

import lancedb
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from openai import OpenAI
from utils.tokenizer import OpenAICompatibleTokenizerWrapper

import glob
import os

load_dotenv()

# Initialize OpenAI client (make sure you have OPENAI_API_KEY in your environment variables)
client = OpenAI()


tokenizer = OpenAICompatibleTokenizerWrapper()  # Load our custom tokenizer for OpenAI
MAX_TOKENS = 8191  # text-embedding-3-large's maximum context length


# --------------------------------------------------------------
# Extract the data
# --------------------------------------------------------------

converter = DocumentConverter()
result = converter.convert("https://www.safetyforward.com/docs/legal.pdf")


# --------------------------------------------------------------
# Apply hybrid chunking
# --------------------------------------------------------------

chunker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=MAX_TOKENS,
    merge_peers=True,
)

chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)

# --------------------------------------------------------------
# Create a LanceDB database and table
# --------------------------------------------------------------

# Create a LanceDB database
db = lancedb.connect("data/lancedb")


# Get the OpenAI embedding function as a function and use text-embedding-3-large model for embedding
func = get_registry().get("openai").create(name="text-embedding-3-large")

#--------------------------------------------------------------
# Defining a simplified metadata schema 
## Schema Definition
#
#-   Defines two Pydantic models:
#    -   `ChunkMetadata`: Stores metadata about each chunk (filename, page numbers, title)
#    -   `Chunks`: Main schema with text content, vector embeddings, and metadata
#--------------------------------------------------------------

class ChunkMetadata(LanceModel):
    """
    You must order the fields in alphabetical order.
    This is a requirement of the Pydantic implementation.
    """

    filename: str | None
    page_numbers: List[int] | None
    title: str | None


# Define the main Schema
class Chunks(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()  # type: ignore
    metadata: ChunkMetadata


table = db.create_table("docling", schema=Chunks, mode="overwrite")

# --------------------------------------------------------------
# Prepare the chunks for the table
# --------------------------------------------------------------

# Create table with processed chunks
processed_chunks = [
    {
        "text": chunk.text,
        "metadata": {
            "filename": chunk.meta.origin.filename,
            "page_numbers": [
                page_no
                for page_no in sorted(
                    set(
                        prov.page_no
                        for item in chunk.meta.doc_items
                        for prov in item.prov
                    )
                )
            ]
            or None,
            "title": chunk.meta.headings[0] if chunk.meta.headings else None,
        },
    }
    for chunk in chunks
]

# --------------------------------------------------------------
# Add the chunks to the table (automatically embeds the text)
# --------------------------------------------------------------

table.add(processed_chunks)

# --------------------------------------------------------------
# Load the table and export to Excel
# --------------------------------------------------------------

# Convert to pandas DataFrame
df = table.to_pandas()
print(f"Total rows in table: {table.count_rows()}")

# Export DataFrame to Excel
excel_path = "data/embedded_chunks.xlsx"
print(f"Exporting data to {excel_path}...")
df.to_excel(excel_path, index=False)
print(f"Data successfully exported to {excel_path}")

# --------------------------------------------------------------
# Search the table
uri = "data/lancedb"
db = lancedb.connect(uri)

# --------------------------------------------------------------
# List all tables in the database
# --------------------------------------------------------------

print("Checking database structure...")
# Check if the database directory exists
if os.path.exists("data/lancedb"):
    print(f"Database directory exists at 'data/lancedb'")
    
    # List all directories in the database (potential tables)
    table_dirs = [d for d in os.listdir("data/lancedb") if os.path.isdir(os.path.join("data/lancedb", d))]
    print(f"Found directories in database: {table_dirs}")
    
    # Check for manifest files which indicate tables
    manifest_files = glob.glob("data/lancedb/**/*.manifest", recursive=True)
    print(f"Found manifest files: {manifest_files}")
else:
    print("Database directory 'data/lancedb' does not exist!")
    print("Make sure you've run Step3-embedding.py first to create and populate the database.")
    exit(1)

# --------------------------------------------------------------
# Try to load the table
# --------------------------------------------------------------

# First try the original table name
try:
    print("Attempting to open table 'docling'...")
    table = db.open_table("docling")
    print("Successfully opened 'docling' table")
except ValueError as e:
    print(f"Error opening 'docling' table: {str(e)}")
    
    # If that fails, try to find any available tables
    try:
        # Try to list all tables in the database
        print("Trying to list all tables in the database...")
        tables = db.table_names()
        print(f"Available tables: {tables}")
        
        if tables:
            # Try to open the first available table
            first_table = tables[0]
            print(f"Attempting to open first available table: '{first_table}'...")
            table = db.open_table(first_table)
            print(f"Successfully opened '{first_table}' table")
        else:
            print("No tables found in the database.")
            print("Make sure you've run Step3-embedding.py first to create and populate the table.")
            exit(1)
    except Exception as e2:
        print(f"Error listing tables: {str(e2)}")
        print("Make sure you've run Step3-embedding.py first to create and populate the table.")
        exit(1)

# --------------------------------------------------------------
# Search the table
# --------------------------------------------------------------

# Only execute this section if the table was successfully opened
if 'table' in locals():
    print("\nPerforming vector search...")
    result = table.search(query="payment of a fee", query_type="vector").limit(5)
    print("\nSearch results:")
    #print(result.to_pandas())
    result.to_pandas()

