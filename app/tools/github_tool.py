from langchain.tools import tool
import requests
from app.core.config import get_settings

config = get_settings()

@tool
def get_repo_info():

    """
      Fetch Prashant's live public GitHub repositories.
      Use this for ANY question about projects — specific project names, 
      what he has built, recent work, or project links.
      Also use alongside RAG when user asks about his work generally.
      Returns repo names, URLs, descriptions and language.
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