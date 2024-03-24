import os
import tokenize
from io import BytesIO

def chunk_and_tokenize_repo(repo_path):
    files_data = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    content = f.read()
                    file_data = {
                        "filename": file,
                        "filepath": file_path,
                        "chunks": chunk_and_tokenize_file(content)
                    }
                    files_data.append(file_data)
    return files_data

def chunk_and_tokenize_file(file_content):
    chunks = []
    current_chunk = []
    current_line = ""
    
    def process_current_chunk():
        if current_chunk:
            chunk_text = "\n".join(current_chunk)
            tokens = list(tokenize.tokenize(BytesIO(chunk_text.encode()).readline))
            chunks.append({"text": chunk_text, "tokens": tokens})
            current_chunk.clear()
    
    for line in file_content.decode().split("\n"):
        line = line.strip()
        if line.startswith(("def ", "class ", "@")) or (current_line and not line):
            process_current_chunk()
        current_chunk.append(line)
        current_line = line
    
    process_current_chunk()
    return chunks

def process_repos(repo_paths):
    all_files_data = []
    for repo_path in repo_paths:
        files_data = chunk_and_tokenize_repo(repo_path)
        all_files_data.extend(files_data)
    return all_files_data

# Example usage
repo_paths = [
    "test_repo",
]

files_data = process_repos(repo_paths)

# Print the file data, including filename, filepath, and chunks with tokens
for file_data in files_data:
    print("Filename:", file_data["filename"])
    print("Filepath:", file_data["filepath"])
    print("Chunks:")
    for chunk in file_data["chunks"]:
        print("  Chunk:")
        print("    Text:", chunk["text"])
        print("    Tokens:")
        for token in chunk["tokens"]:
            print("      ", token)
    print("---")