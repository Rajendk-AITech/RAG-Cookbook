import lancedb
import os
import glob

# --------------------------------------------------------------
# Connect to the database
# --------------------------------------------------------------

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
    result = table.search(query="what's docling?", query_type="vector").limit(3)
    print("\nSearch results:")
    print(result.to_pandas())
