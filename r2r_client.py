import asyncio
import os
import uuid

from r2r.client import R2RClient

# Initialize the client with the base URL of your API
base_url = "https://sciphi-28cd5f4f-be79-4ef6-be81-eabd9e88ab40-qwpin2swwa-ue.a.run.app"
client = R2RClient(base_url)


def upload_data():
    print("Upserting entry to remote db...")
    folder_path = 'data'
    # Uploading the tips and data folder content
    entries = []
    for filename in os.listdir('data'):
        # Check if the file has a .txt extension
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            
            # Open the file and read its content
            with open(file_path, "r") as file:
                content = file.read()
                
                # # Print the filename and its content
                # print(f"File: {filename}")
                # print("Content:")
                # print(content)
                # print("---")
                entries.append(
                {
                    "document_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{filename}")),
                    "blobs": {"txt": content},
                    "metadata": {"tags": "tips"},
                }
                )

    bulk_upsert_response = client.add_entries(entries, do_upsert=True)
    print(f"Upsert entries response:\n{bulk_upsert_response}\n\n")


def normal_search():
    # Perform a search
    print("Searching remote db...")
    search_response = client.search("test", 5)
    print(f"Search response:\n{search_response}\n\n")


def filtered_search(query, limit=3, filters={"tags": "tips"}):
    print("Searching remote db with filter...")
    # Perform a search w/ filter
    filtered_search_response = client.search(query, limit, filters=filters)
    print(f"Search response w/ filter:\n{filtered_search_response}\n\n")
    return filtered_search_response


# print("Fetching logs after all steps...")
# logs_response = client.get_logs()
# print(f"Logs response:\n{logs_response}\n")

# print("Fetching logs summary after all steps...")
# logs_summary_response = client.get_logs_summary()
# print(f"Logs summary response:\n{logs_summary_response}\n")

if __name__=="__main__":
    # upload_data()
    filtered_search("How to optimize my code?")