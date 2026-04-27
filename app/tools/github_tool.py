from fastapi import HTTPException
from langchain.tools import tool
import requests
from app.core.config import get_settings

config = get_settings()

@tool
def get_repo_info():

    """
      Fetch Prashant's live public GitHub repositories.
      Use this ONLY when the user explicitly asks about his GitHub,
      his repos, what he has built recently, or wants project links.
      Do NOT use this for general project questions — use the RAG tool for those.
      Returns a formatted list of repo names, urls, descriptions and language.
    """

    response = requests.get(config.GITHUB_BASE_URL)
    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception("GitHub API request failed. Please try again later.")
   
    return [
            {
                "repo_name":content.get("name",""),
                "url":content.get("html_url",""),
                "description":content.get("description",""),
                "language":content.get("language","")
            }
        for content in data
    ]