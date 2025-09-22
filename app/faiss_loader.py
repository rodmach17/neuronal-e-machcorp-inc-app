from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Modelo de embeddings optimizado para CPU
embedding_model = HuggingFaceEmbeddings(
    model_name="hkunlp/instructor-base",
    model_kwargs={"device": "cpu"}
)

# Cargar índice FAISS (ya generado)
vectorstore = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

def get_answer(query: str) -> str:
    docs = vectorstore.similarity_search(query, k=1)
    return docs[0].page_content if docs else "No se encontró una respuesta relevante."