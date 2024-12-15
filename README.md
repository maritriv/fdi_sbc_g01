# Virtual Assistant with Knowledge Base Integration

![Alt text](https://static.vecteezy.com/system/resources/previews/023/485/861/non_2x/talking-robot-graphic-clipart-design-free-png.png)


This project implements a command-line virtual assistant powered by a knowledge base and a language model. The assistant provides detailed, conversational answers and supports reasoning by leveraging the knowledge base and the language model for queries.

## Features
- Interactive command-line interface (CLI) using Click.
- Integration with external knowledge bases.
- Reasoning capabilities with chain-of-thought refinement.
- Temporary conversation history for contextual responses.
- Entity extraction from the knowledge base to enhance query results.

## Usage

Run the `main.py` script from the command line:

```bash
python main.py <knowledge_base_file> [--model <model_name>] [--verbose]
```

### Arguments
- `<knowledge_base_file>`: Path to the knowledge base file (required).
- `--model`: Specify the language model to use (default: `llama3.2:1b`).
- `--verbose`: Enable detailed output for debugging (optional).

### Example
```bash
python main.py knowledge_base.txt --model llama3.2:1b --verbose
```

---

## Project Structure

### 1. `main.py`
- **Description**: The entry point for the assistant, responsible for loading the knowledge base, handling user interaction, and querying the language model.
- **Key Functionality**:
  - CLI management with Click.
  - Dynamic conversation handling with temporary files.
  - Integration with knowledge base and RAG (Retrieval-Augmented Generation) pipeline.

### 2. `assistant.py`
- **Description**: Handles querying the language model responses.
- **Functions**:
  - `query_model(query, knowledge_base, conversation_context, model)`: Sends user queries to the language model and generates responses.

### 3. `knowledge_base.py`
- **Description**: Provides utilities to load the knowledge base from a file.
- **Functions**:
  - `load_knowledge_base(file_path)`: Reads the knowledge base file and returns its content as a string.

### 4. `rag.py`
- **Description**: Implements the RAG pipeline for extracting entities and generating query-specific answers.
- **Functions**:
  - `rag(knowledge_base, model)`: Extracts entities from the knowledge base for contextual relevance.
  - `rag_query(query, entities, model)`: Queries the extracted entities for more accurate responses.

### 5. `chain_of_thought.py`
- **Description**: Handles the refining responses of the model.
- **Functions**:
  - `chain_of_thought(response, model)`: Refines initial responses to ensure clarity and confidence.
---

## Requirements
- Python 3.8+
- Required libraries:
  - `Click`
  - `tempfile`
  - `ollama`
  - Additional dependencies specified in `requirements.txt`

---

## How It Works
1. **Knowledge Base Loading**: The specified file is loaded into memory as a string and divided into paragraphs.
2. **Entity Extraction**: The RAG pipeline identifies entities (people, places, or organizations) to enhance query accuracy.
3. **Query Handling**: User queries are processed using the knowledge base and model. The conversation context is stored temporarily for coherence.
4. **Chain of Thought**: Responses are refined to ensure clarity and thoroughness.
5. **Interactive Session**: Users can ask questions, receive detailed answers, and exit the session with the `exit` command.

---

## Authors
This projetct has been done by Marina Triviño de las Heras and Pablo Alonso Romero.
