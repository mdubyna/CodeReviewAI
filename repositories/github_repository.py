import httpx
from logging import getLogger

import config


logger = getLogger(__name__)

class GitHubRepository:
    """
    A repository class for interacting with the GitHub API to fetch repository file content and structure.
    """

    BASE_URL = "https://api.github.com"

    async def fetch_repository_files(self, repo_url: str, path: str = "") -> tuple[str, str]:
        """
           Fetches the content and structure of files from a GitHub repository.

           Args:
               repo_url (str): The URL of the GitHub repository (e.g., "https://github.com/owner/repo").
               path (str): Optional. The path inside the repository to fetch. Defaults to the root.

           Returns:
               tuple[str, str]: A tuple containing:
                   - A string representing the concatenated content of all files matching the criteria.
                   - A string representing the hierarchical structure of the repository files and directories.

           Notes:
               - Files and directories are filtered based on `config.FILES_FOR_REVIEWING`,
                 `config.EXCLUDED_FILE_NAMES`, and `config.EXCLUDED_DIR_NAMES`.
               - Requires a valid GitHub API token to be set in `config.GITHUB_TOKEN`.
        """

        api_url = repo_url.replace("https://github.com/", f"{self.BASE_URL}/repos/")
        api_url += f"/contents/{path}" if path else "/contents"

        headers = {"Authorization": f"token {config.GITHUB_TOKEN}"}

        async with (httpx.AsyncClient() as client):
            response = await client.get(api_url, headers=headers)
            if response.status_code != 200:
                logger.info(
                    "An error occurred when trying to fetch data from github. Status code: %s",
                    response.status_code
                )
                return "", ""

            data = response.json()

            all_code = []
            repo_structure_lines = []

            for item in data:
                if  (
                    item["type"] == "file"
                    and item["name"].endswith(config.FILES_FOR_REVIEWING)
                    and item["name"] not in config.EXCLUDED_FILE_NAMES
                ):
                    logger.error("Processing github repo file: %s", item["name"])
                    # Fetch file content
                    file_response = await client.get(item["download_url"])
                    file_content = await file_response.aread()
                    all_code.append(f"# File: {item['path']}\n{file_content}\n\n")

                    repo_structure_lines.append(item["path"])

                elif item["type"] == "dir" and item["name"] not in config.EXCLUDED_DIR_NAMES:
                    # Recursively fetch subdirectory content and structure
                    subdir_code, subdir_structure = await self.fetch_repository_files(repo_url, item["path"])
                    all_code.append(subdir_code)
                    repo_structure_lines.append(subdir_structure)

        return "\n".join(all_code), "\n".join(filter(None, repo_structure_lines))
