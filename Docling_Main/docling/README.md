# **Creating a Robust Knowledge Extraction Pipeline with Docling**  

[Docling](https://github.com/docling-project/docling) is a powerful and flexible open-source document processing library that transforms various document formats into a unified structure. It leverages cutting-edge AI models for **layout analysis** and **table structure recognition**, allowing for deeper document understanding.  

Designed to run locally on standard computers, Docling is highly **extensible**—developers can integrate new models or customize pipelines for specific use cases. It is particularly valuable for **enterprise document search, passage retrieval, and knowledge extraction**. With its advanced segmentation and processing capabilities, Docling is a powerful tool for **Retrieval-Augmented Generation (RAG)-based AI applications**.  

---

## **Key Features**  
- **Multi-Format Support** – Process PDF, DOCX, XLSX, PPTX, Markdown, HTML, images, and more  
- **AI-Powered Understanding** – Layout analysis and table structure recognition  
- **Flexible Output Formats** – Export data as HTML, Markdown, JSON, or plain text  
- **High Performance** – Runs efficiently on local hardware  

---

## **Upcoming Features**  
Docling continues to evolve, with the following features in development:  
- Metadata extraction (title, authors, references, language)  
- Support for **SmolDocling**, a lightweight Visual Language Model  
- Chart analysis (Bar charts, Pie charts, Line plots, etc.)  
- Advanced chemistry document parsing (Molecular structure recognition)  

---

### Prerequisites

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Set up your environment variables by creating a `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

### Running the Example

Execute the files in order to build and query the document database:

1. Extract document content: `python Step1-extraction.py`
2. Create document chunks: `python Step2-chunking.py`
3. Create embeddings and store in LanceDB: `python Step3-embedding.py`
4. Test basic search functionality: `python Step4-search.py`
5. Launch the Streamlit chat interface: `streamlit run Step5-chat.py`

Then open your browser and navigate to `http://localhost:8501` to interact with the document Q&A interface.
Once the server is running, navigate to **[http://localhost:8501](http://localhost:8501/)** to interact with the **document Q&A system**.

----------

## **Supported Document Formats**

## **Supported Document Formats**  

| **Format**             | **Description**                                      |
|------------------------|------------------------------------------------------|
| **PDF**               | Native PDF documents with structure preservation     |
| **DOCX, XLSX, PPTX**  | Microsoft Office files (Word, Excel, PowerPoint)    |
| **Markdown**          | Text with markup                                    |
| **HTML/XHTML**        | Web documents                                      |
| **Images**            | PNG, JPEG, TIFF, BMP                               |
| **USPTO XML**         | Patent documents                                   |
| **PMC XML**           | PubMed Central articles                            |

For a complete and **updated list**, refer to [this page](https://docling-project.github.io/docling/usage/supported_formats/) .

----------

## **Processing Pipeline**

The document processing workflow includes:

1.  **Parsing** – Format-specific document extraction
2.  **Layout Analysis** – AI-based page element detection
3.  **Table Structure Recognition** – Identifying complex table layouts
4.  **Metadata Extraction** – Extracting key document attributes
5.  **Content Structuring** – Organizing extracted content intelligently
6.  **Exporting** – Formatting content for AI applications

----------

## **AI Models Powering Docling**

Docling utilizes **state-of-the-art AI models** for accurate and efficient **document comprehension**:

### **1. Layout Analysis Model**

-   Built on **RT-DETR (Real-Time Detection Transformer)**
-   Processes pages at **72 dpi** in **under a second on a standard CPU**
-   Trained on the **DocLayNet dataset**

### **2. Table Structure Recognition Model – TableFormer**

-   Handles complex tables (empty cells, spanning cells, hierarchical headers)
-   Processes tables in **2-6 seconds on CPU**

### **3. OCR for Image-based Text Extraction**

-   Integrated **EasyOCR** for image-to-text conversion
-   Works at **216 dpi** for optimal quality, processing one page in **~30 seconds**

Both **layout analysis** and **TableFormer models** are developed by **IBM Research** and can be found on **Hugging Face** under ["ds4sd/docling-models"](https://huggingface.co/ds4sd/docling-models) .

For a technical deep dive, check out the **[research paper](https://arxiv.org/pdf/2408.09869)** .

----------

## **Advanced Chunking for RAG Applications**

For **Retrieval-Augmented Generation (RAG)** applications, document chunking plays a crucial role in **optimizing search** and **retrieval efficiency**.

Unlike naive text-splitting, Docling's **intelligent chunking** preserves document structures using two primary approaches:

### **1. Hierarchical Chunker**

-   Identifies **natural section boundaries** such as
    -   Headers, paragraphs, tables, and lists
    -   Maintains relationships between headings and their content

### **2. Hybrid Chunker**

-   Enhances hierarchical chunks by:
    -   Splitting oversized chunks based on the embedding model
    -   Merging small chunks to ensure meaningful retrieval
    -   Optimizing chunks for **language model tokenization**

### **Why This Matters for RAG Applications**

A poorly structured chunking approach (e.g., cutting text every 500 words) can:  
❌ Break tables into meaningless fragments  
❌ Disconnect headers from their corresponding content

With **Docling’s intelligent chunking**, RAG applications benefit from:  
✅ Preserved document structure  
✅ Context-aware retrieval (headings, captions, etc.)  
✅ Improved **semantic understanding** for AI models  
✅ **Optimized query responses**

For more details, explore [Docling’s Chunking Concepts](https://docling-project.github.io/docling/examples/hybrid_chunking/) .

----------

## **Further Resources**

-   **📖 Official Documentation:** [Docling Docs](https://docling-project.github.io/docling/)
-   **🔬 Example Notebooks & Guides:** [GitHub Repository](https://github.com/docling-project/docling)
-    🛢️  **LanceDB DOCs**  [Lance DB](https://github.com/lancedb/lancedb)


Explore **Docling** and start building intelligent **knowledge extraction pipelines today! 🚀**
