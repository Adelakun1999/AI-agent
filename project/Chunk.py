from data_ingestion import read_repo_data

rag_cookbook = read_repo_data('athina-ai' , 'rag-cookbooks')

def sliding_window(seq , size , step):
    if size <=0 or step <=0:
        raise ValueError("size and step must be positive")
    
    n = len(seq)
    result = []
    for i in range(0 , n , step):
        chunk = seq[i:i+size]
        result.append({'start' : i , 'chunk' : chunk})
        if i + size >=n:
            break 
            
    return result 



rag_chunks = []

for doc in rag_cookbook:
    doc_copy = doc.copy()
    doc_content = doc_copy.pop('content')
    chunks = sliding_window(doc_content ,2000 , 1000)
    for chunk in chunks:
        chunk.update(doc_copy)
    rag_chunks.extend(chunks)