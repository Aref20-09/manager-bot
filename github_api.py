import base64
import requests
from settings import GITHUB_TOKEN

def update_file(repo, path, new_content):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    get_file = requests.get(url, headers=headers)

    if get_file.status_code == 404:
        print("فایل پیدا نشد:", path)
        return False

    data_json = get_file.json()
    sha = data_json.get("sha")

    data = {
        "message": f"Update {path} via manager bot",
        "content": base64.b64encode(new_content.encode()).decode(),
        "sha": sha
    }

    response = requests.put(url, headers=headers, json=data)
    print("GitHub status:", response.status_code, response.text)

    return response.status_code in (200, 201)
