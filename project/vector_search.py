#text search
from minsearch import Index
from minsearch import VectorSearch
from data_ingestion import read_repo_data
from sentence_transformers import SentenceTransformer
from chunk import rag_chunking
import numpy as np

rag_cookbook = read_repo_data('athina-ai' , 'rag-cookbooks')

index = Index(
    text_field = ["chunk", "title", "description", "filename"] , 
    keyword_fields=[]

)

chunks = rag_chunking(rag_cookbook)

index.fit(chunks)


# Vector search
embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")
faq_embeddings = []

for chunk in chunks:
    text = chunk['chunk']
    v = embedding_model.encode(text)
    faq_embeddings.append(v)

faq_embeddings = np.array(faq_embeddings)

faq_vindex = VectorSearch()
faq_vindex.fit(faq_embeddings, chunks)


def text_search(query):
    results = index.search(query ,num_results=5)
    return results

def vector_search(query):
    query_embedding = embedding_model.encode(query)
    results = faq_vindex.search(query_embedding , num_results=5)
    return results


def hybrid_search(query):
    text_results = text_search(query)
    vector_results = vector_search(query)

    #combine and duplicates result 
    seen_ids = set()
    combined_results = []

    for result in text_results + vector_results:
        if result['filename'] not in seen_ids:
            seen_ids.add(result['filename'])
            combined_results.append(result)

    return combined_results