# utils.py

from datetime import timedelta, time, datetime

from config.configuration import getDay

def getDateArray(current_date):
    dates = []
    dates.insert(0, current_date)
    element = getDay()
    day = 1
    while True:
        if day > element - 1:
            break
        temp_date = dates[0] - timedelta(days=1)
        dates.insert(0, temp_date)
        day += 1
    return dates

def getCurrentStartDate():
    current_date = datetime.now().date()
    return datetime.combine(current_date, time(0, 0, 0))

def parseDate(dateStr):
    if dateStr is not None:
        dateStr = dateStr.replace('T', ' ').replace('Z', '')
        return datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
    
def addCount(item, obj):
    if item['security_severity_level'] == 'critical':
        obj['critical'] += 1
    elif item['security_severity_level'] == 'high':
        obj['high'] += 1
    elif item['security_severity_level'] == 'medium':
        obj['medium'] += 1
    else:
        obj['low'] += 1
    
def summarizeIssue(items):
    summary = []
    dateArray = getDateArray( getCurrentStartDate() )

    for dateTemp in dateArray:
        key = dateTemp.strftime('%Y-%m-%d')
        temp_obj = {
            'date': key,
            'open': {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            },
            'close': {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            }
        }

        for item in items:
            if item['state'] == 'open':
                addCount(item, temp_obj['open'])
            elif item['fixedDate'] > dateTemp:
                addCount(item, temp_obj['open'])
            else:
                addCount(item, temp_obj['close'])
        summary.append(temp_obj)
    return summary

def findItem(results, item):
    findOne = None
    for result in results:
        if result['date'] == item['date']:
            findOne = result
            break
    return findOne

def calTotal(summarys):
    results = []
    for summary in summarys:
        for temp in summary:
            targetItem = findItem(results, temp)
            if targetItem is None:
                targetItem = {
                    'date': temp['date'],
                    'open': {
                        'critical': temp['open']['critical'],
                        'high': temp['open']['high'],
                        'medium': temp['open']['medium'],
                        'low': temp['open']['low']
                    },
                    'close': {
                        'critical': temp['close']['critical'],
                        'high': temp['close']['high'],
                        'medium': temp['close']['medium'],
                        'low': temp['close']['low'],
                    }
                }
                results.append(targetItem)
            else:
                targetItem['open']['critical'] = targetItem['open']['critical'] + temp['open']['critical']
                targetItem['open']['high'] = targetItem['open']['high'] + temp['open']['high']
                targetItem['open']['medium'] = targetItem['open']['medium'] + temp['open']['medium']
                targetItem['open']['low'] = targetItem['open']['low'] + temp['open']['low']
                targetItem['close']['critical'] = targetItem['close']['critical'] + temp['close']['critical']
                targetItem['close']['high'] = targetItem['close']['high'] + temp['close']['high']
                targetItem['close']['medium'] = targetItem['close']['medium'] + temp['close']['medium']
                targetItem['close']['low'] = targetItem['close']['low'] + temp['close']['low']
    return results

def calAllTotal(repoIssues):
    results = []
    for issue in repoIssues:
        total = issue['openCount'] + issue['closeCount']    
        item = [issue['repo'], issue['openCount'], issue['closeCount'], total]
        results.append(item)
    return results