import aiohttp
import asyncio
import ssl
import certifi
from datetime import datetime, timedelta
from keys import github_token

# Ваши данные
org_names = ['paritytech']
headers = {
    'Authorization': github_token,  # Замените на ваш GitHub токен
    'Accept': 'application/vnd.github.v3+json',
}

# Создаем SSL контекст с сертификатами от Certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

async def fetch_json(session, url):
    async with session.get(url, ssl=ssl_context, headers=headers) as response:
        return await response.json()

async def get_all_repos(session, org_name):
    repos = []
    page = 1
    while True:
        url = f'https://api.github.com/orgs/{org_name}/repos?page={page}&per_page=100'
        page_repos = await fetch_json(session, url)
        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1
    return repos

async def count_commits(session, repo, since):
    commits_url = repo['commits_url'].replace('{/sha}', f'?since={since}')
    return len(await fetch_json(session, commits_url))

async def main():
    async with aiohttp.ClientSession() as session:
        since_date = (datetime.now() - timedelta(days=30)).isoformat()
        out = dict()
        for org_name in org_names:
            total_commits = 0
            repos = await get_all_repos(session, org_name)
            for repo in repos:
                if not repo['fork']:
                    commits = await count_commits(session, repo, since_date)
                    total_commits += commits
                    print(f"Количество коммитов в репозитории {repo['name']}: {commits}")

            out[org_name] = total_commits
        sorted_dict = dict(sorted(out.items(), key=lambda item: item[1], reverse=True))
        output = [f'{key} : {value}' for key, value in sorted_dict.items()]
        print('\n'.join(output))

asyncio.run(main())
