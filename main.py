import requests
import os

# Define the folder path
folder_path = "crawled_data"

# Check if the folder exists; if not, create it
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

api_url = "https://www.erfgoedleiden.nl/opensearch/"
per_page = 100  # Number of results per page
params = {
    "q": "*",
    "limit": per_page,
    "page": 1  # Start with page 1
}

# to get total number of results we only need to fetch
params["limit"] = 1
response = requests.get(api_url, params=params)

if response.status_code == 200:
    total_results = int(response.text.split('<opensearch:totalResults>')[1].split('</opensearch:totalResults>')[0])
    #num_pages = (total_results + per_page - 1) // per_page  # Calculate the number of pages
    num_pages = 2
    
    # put back the limit
    params["limit"] = per_page

    for page in range(1, num_pages + 1):
        params["page"] = page
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            # Save the XML response to a file
            page_filename = os.path.join(folder_path, f"page_{params['page']}_results.xml")
            with open(page_filename, "w") as file:
                file.write(response.text)        
        else:
            print(f"Error: Failed to retrieve data from page {page}")
else:
    print("Error: Failed to retrieve data from the API")
