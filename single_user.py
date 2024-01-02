import requests
from datetime import datetime, timedelta

def get_user_commits(username, month_ago):
    # Подготовка дат
    start_date = month_ago.strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    # Получение списка репозиториев пользователя
    repos_response = requests.get(f'https://api.github.com/users/{username}/repos')
    repos = repos_response.json()

    total_commits = 0

    # Перебор репозиториев и подсчет коммитов
    for repo in repos:
        if not repo['fork']:
            commits_response = requests.get(
                f'https://api.github.com/repos/{username}/{repo["name"]}/commits',
                params={'since': start_date, 'until': end_date}
            )
            commits = commits_response.json()
            total_commits += len(commits)

    return total_commits

# Пример использования
username = 'LongWeeeeeee'
month_ago = datetime.now() - timedelta(days=30)
commits = get_user_commits(username, month_ago)
print(f'Количество коммитов за последний месяц: {commits}')
