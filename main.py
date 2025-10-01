import requests
import io 
import frontmatter
import zipfile


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
                data["filename"] = filename
                repository_data.append(data)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    zf.close()
    return repository_data
    