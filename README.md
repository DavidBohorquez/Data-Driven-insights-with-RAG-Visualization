# Data-Driven-insights-with-RAG-Visualization
System that leverages Retrieval-Augmented Generation (RAG) with a Large Language Model (LLM) to answer user questions about a dataset and generate visualizations based on the retrieved data. The project demonstrates the integration of SQL databases, LLMs, and data visualization tools to provide data-driven insights in natural language.

## Project Overview

TorusAI is a Proof of Concept (POC) system that leverages **Retrieval-Augmented Generation (RAG)** with a Large Language Model (LLM) to answer user questions about a dataset and generate visualizations based on the retrieved data. The project demonstrates the integration of SQL databases, LLMs, and data visualization tools to provide data-driven insights in natural language.

### Key Features
- **Natural Language Querying**: Users can ask questions in plain language.
- **SQL Query Generation**: The system dynamically generates SQL queries using a fine-tuned LLM.
- **Data Retrieval**: Queries are executed against a relational SQL database.
- **LLM Response**: The retrieved data is passed to the LLM for generating a natural language response.
- **Visualization**: Users can request visualizations (e.g., bar charts) based on the data.

---

## Prerequisites

Before running the project, ensure you have the following installed:
- **Python 3.9+**
- **Docker** and **Docker Compose**
- **Git**

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DavidBohorquez/Data-Driven-insights-with-RAG-Visualization.git
   cd Data-Driven-insights-with-RAG-Visualization