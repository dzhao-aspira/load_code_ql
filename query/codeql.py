# codeql.py

import requests

from util.utils import parseDate
from config.configuration import getOwner, getToken

access_token = getToken()
owner = getOwner()
headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json'
}

def queryIssue(repo):
    page = 1
    alerts = []
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/code-scanning/alerts?tool_name=CodeQL&per_page=100&page={page}'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
                print(f'Error: {response.status_code}')
                break
        results = response.json()
        if not results:
            break
        alerts.extend(results)
        page += 1
    return alerts

def calIssueCount(items, repo):
    data = {
        'repo': repo,
        'openCount': 0,
        'closeCount': 0,
        'items':[]
    }

    for alert in items:
        if alert['state'] == 'open':
            data['openCount'] += 1
        else:
            data['closeCount'] += 1
        
        dismissedBy = ''
        if alert['state'] == 'dismissed':
            dismissedBy = alert['dismissed_by']['login']
        item = {
            'number': alert['number'],
            'state':alert['state'],
            'url':alert['html_url'],
            'createDate':parseDate(alert['created_at']),
            'fixedDate':parseDate(alert['fixed_at']),
            'dismissedDate': parseDate(alert['dismissed_at']),
            'dismissedReason': alert['dismissed_comment'],
            'dismissedBy': dismissedBy,
            'security_severity_level': alert['rule']['security_severity_level'],
            'description': alert['rule']['description'],
            'rule': alert['rule']['id'],
            'location': alert['most_recent_instance']['location']['path'],
            'line': alert['most_recent_instance']['location'].get('start_line', ''),
        }
        data['items'].append(item)
    return data


def loadIssue(repos):
    repoIssue = []
    for repo in repos:
        print(f'Load CodeQL data from git for {repo}')
        result = queryIssue(repo)      
        repoIssue.append(calIssueCount(result, repo))
    return repoIssue
