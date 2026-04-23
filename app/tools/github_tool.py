
from fastapi import HTTPException
import requests

BASE_URL = "https://api.github.com/users/prashant00797/repos"

def get_repo_info():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
    else:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. Please Try again later"
        )
   
    return [
            {
                "repo_name":content.get("name",""),
                "url":content.get("html_url",""),
                "description":content.get("description",""),
                "language":content.get("language","")
            }
        for content in data
    ]

# test  
# res = get_repo_info()
# print(res)