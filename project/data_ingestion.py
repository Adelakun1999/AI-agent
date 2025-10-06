import requests
import io 
import frontmatter
import zipfile
from minsearch import Index


def read_repo_data(repo_owner , repo_name):
    prefix = "https://codeload.github.com"
    url = f"{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/main"
    resp = requests.get(url)

    if resp.status_code != 200:
        raise Exception(f"Failed to download repo: {resp.status_code}")
    
    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename
        filename_lower = filename.lower()

        if not (filename_lower.endswith('.md') or filename_lower.endswith('.mdx')):
            continue

        try:
            with zf.open(file_info) as f_in:
                content = f_in.read().decode('utf-8' , errors='ignore')
                post = frontmatter.loads(content)
                data = post.to_dict()
                _, filename_repo = file_info.filename.split('/', maxsplit=1)
                data["filename"] = filename_repo
                repository_data.append(data)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    zf.close()
    return repository_data




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


def rag_chunking(documents , size=500 , step= 200):
    rag_chunks = []
    for doc in documents:
        doc_copy = doc.copy()
        doc_content = doc_copy.pop('content')
        chunks = sliding_window(doc_content , size , step)
        for chunk in chunks:
            chunk.update(doc_copy)
        rag_chunks.extend(chunks)
        
    return chunks


def index_data(
        repo_owner , 
        repo_name ,
        
):
    docs = read_repo_data(repo_owner , repo_name)
    
    chunk_docs = rag_chunking(docs)

    index = Index(
        text_fields = ["chunk", "title", "description", "filename"] , 
        keyword_fields=[]
    )
    index.fit(chunk_docs)
    return index



    