"""
RAG (Retrieval-Augmented Generation) System for FitBuddy
Uses ChromaDB for vector storage and LangChain for document processing
"""

import os
from typing import List, Dict
from pathlib import Path
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document


class FitnessKnowledgeBase:
    """Manages the fitness and nutrition knowledge base using RAG"""
    
    def __init__(self, persist_directory: str = "./chroma_db", openai_api_key: str = None):
        """
        Initialize the knowledge base
        
        Args:
            persist_directory: Directory to store the vector database
            openai_api_key: OpenAI API key for embeddings (if None, loads from environment)
        """
        load_dotenv()
        
        self.persist_directory = persist_directory
        
        # Set up OpenAI API key for embeddings
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        else:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            print("Warning: OPENAI_API_KEY not found. Embeddings may not work properly.")
        
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )
    
    def load_documents_from_directory(self, directory_path: str) -> List[Document]:
        """
        Load text documents from a directory
        
        Args:
            directory_path: Path to directory containing text files
            
        Returns:
            List of Document objects
        """
        documents = []
        directory = Path(directory_path)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        for file_path in directory.glob("*.txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                doc = Document(
                    page_content=content,
                    metadata={"source": file_path.name}
                )
                documents.append(doc)
        
        return documents
    
    def create_vectorstore(self, documents: List[Document]) -> None:
        """
        Create and persist the vector store from documents
        
        Args:
            documents: List of Document objects
        """
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"Created vector store with {len(chunks)} chunks")
    
    def load_vectorstore(self) -> None:
        """Load existing vector store from disk"""
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(
                f"Vector store not found at {self.persist_directory}. "
                "Create it first using create_vectorstore()."
            )
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        print(f"Loaded vector store from {self.persist_directory}")
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Search the knowledge base for relevant information
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents with content and metadata
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Load or create it first.")
        
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "relevance_score": float(score)
            })
        
        return formatted_results
    
    def get_context_for_query(self, query: str, k: int = 3) -> str:
        """
        Get formatted context for a query to use in LLM prompts
        
        Args:
            query: Search query
            k: Number of results to include
            
        Returns:
            Formatted context string
        """
        results = self.search(query, k=k)
        
        context = "Relevant information from fitness and nutrition guides:\n\n"
        for i, result in enumerate(results, 1):
            context += f"{i}. From {result['source']}:\n"
            context += f"{result['content']}\n\n"
        
        return context


def initialize_knowledge_base(knowledge_dir: str = "./knowledge_base", 
                            persist_dir: str = "./chroma_db",
                            force_rebuild: bool = False,
                            openai_api_key: str = None) -> FitnessKnowledgeBase:
    """
    Initialize or load the fitness knowledge base
    
    Args:
        knowledge_dir: Directory containing text documents
        persist_dir: Directory to persist vector database
        force_rebuild: If True, rebuild the vector store even if it exists
        openai_api_key: OpenAI API key for embeddings (required for RAG)
        
    Returns:
        Initialized FitnessKnowledgeBase instance
    """
    kb = FitnessKnowledgeBase(persist_directory=persist_dir, openai_api_key=openai_api_key)
    
    # Check if vector store already exists
    if os.path.exists(persist_dir) and not force_rebuild:
        print("Loading existing vector store...")
        kb.load_vectorstore()
    else:
        print("Creating new vector store...")
        documents = kb.load_documents_from_directory(knowledge_dir)
        kb.create_vectorstore(documents)
    
    return kb
