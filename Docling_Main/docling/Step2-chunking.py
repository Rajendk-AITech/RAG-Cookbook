from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from openai import OpenAI
from utils.tokenizer import OpenAICompatibleTokenizerWrapper

load_dotenv()

# Initialize OpenAI client (make sure you have OPENAI_API_KEY in your environment variables)
client = OpenAI()


tokenizer = OpenAICompatibleTokenizerWrapper()  # Load our custom tokenizer for OpenAI
MAX_TOKENS = 8191  # text-embedding-3-large's maximum context length


# --------------------------------------------------------------
# Extract the data
# https://www.apple.com/newsroom/pdfs/fy2024-q1/FY24_Q1_Consolidated_Financial_Statements.pdf
# --------------------------------------------------------------

converter = DocumentConverter()
result = converter.convert("https://www.safetyforward.com/docs/legal.pdf")


# --------------------------------------------------------------
# Apply hybrid chunking
# --------------------------------------------------------------

chunker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=MAX_TOKENS,
    merge_peers=True, #put smaller chunks together
)

chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)

# Print each chunk on a separate line with an index
print("Chunks:")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:")
    print(chunk)
    print("-" * 50)  # Separator between chunks

print("Number of chunks:", len(chunks))
