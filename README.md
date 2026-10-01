# Enterprise Agentic RAG

🚧 **Status: In progress**

An agentic Retrieval-Augmented Generation (RAG) application being developed with LangGraph, Portkey LLM Gateway, and Gemini Embeddings.

The project aims to retrieve relevant technical information while reducing irrelevant retrieval through semantic reranking, conversation-aware planning, and input/output guardrails.

## Planned Capabilities

The following describes the intended scope. Implementation and testing are ongoing.

- **Agent Orchestration:** LangGraph for query planning, retrieval, response generation, and conversation memory.
- **Guardrails:** NeMo Guardrails for handling off-topic requests, prompt injection, and unsafe inputs or outputs.
- **LLM Gateway:** Portkey for routing model requests and configuring fallback behavior.
- **Document Retrieval:** Qdrant Cloud for vector search and FlashRank for semantic reranking.
- **Embeddings:** Gemini embeddings for representing document content and queries.
- **Document Parsing:** Local parsing of PDF, HTML, TXT, DOCX, and PPTX files.
- **Observability:** LangSmith and Pydantic Logfire for tracing and debugging.
- **Evaluation:** RAGAS-based evaluation of retrieval and response quality.

