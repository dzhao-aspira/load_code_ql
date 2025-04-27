# excelutils.py

import xlsxwriter

from util.utils import getCurrentStartDate

def createFile():
    currentDate = getCurrentStartDate()
    fileName = 'CodeQL_' + currentDate.strftime('%y_%m_%d') + '.xlsx'
    workbook = xlsxwriter.Workbook(fileName)
    return workbook

def saveFile(workbook):
    workbook.close()

def createSheet(workbook, name):
    return workbook.add_worksheet(name)

def writeTotal(workbook, worksheet, datas, repo, startRow):
    print(f'Start write {repo}')
    merge_format = workbook.add_format({'align': 'center','bold': True,'font_color': 'red','bg_color': 'yellow','border': 1 })
    worksheet.merge_range(first_row=startRow, first_col=0, last_row=startRow, last_col=3, data=repo, cell_format=merge_format)
    startRow = startRow + 1
    cell_format = workbook.add_format({
        'bold': True,
        'font_color': 'red',
        'bg_color': 'yellow',
        'border': 1
    })
    header = ['Repo', 'Open', 'Close', 'Total']
    for i, value in enumerate(header):
        worksheet.write(startRow, i, value, cell_format)
    startRow = startRow + 1
    
    for i, row in enumerate(datas, start=startRow):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)
        startRow = startRow + 1
    return startRow


def writeSummary(workbook, worksheet, datas, repo, startRow, sheetName):
    print(f'Write Summary for {repo}')
    firstRow = startRow
    merge_format = workbook.add_format({'align': 'center','bold': True,'font_color': 'red','bg_color': 'yellow','border': 1 })
    worksheet.merge_range(first_row=startRow, first_col=0, last_row=startRow, last_col=8, data=repo, cell_format=merge_format)
    startRow = startRow + 1
    worksheet.merge_range(first_row=startRow, first_col=1, last_row=startRow, last_col=4, data='Open', cell_format=merge_format)
    worksheet.merge_range(first_row=startRow, first_col=5, last_row=startRow, last_col=8, data='Close', cell_format=merge_format)

    startRow = startRow + 1
    header = ["Date", "Critical", "High", "Medium", "Low", "Critical", "High", "Medium", "Low"]
    cell_format = workbook.add_format({
        'bold': True,
        'font_color': 'red',
        'bg_color': 'yellow',
        'border': 1
    })

    for i, value in enumerate(header):
        worksheet.write(startRow, i, value, cell_format)
    worksheet.set_column(0, 0, 15)
    startRow = startRow + 1

    contents = []
    for temp in datas:
        temp_row = [temp['date'], temp['open']['critical'], temp['open']['high'], temp['open']['medium'], temp['open']['low'], 
                    temp['close']['critical'], temp['close']['high'], temp['close']['medium'], temp['close']['low']]
        contents.append(temp_row)
    
    for i, row in enumerate(contents, start=startRow):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)
        startRow = startRow + 1

    chart = workbook.add_chart({'type': 'line'})
    chart.set_size({'width': 700, 'height': 300})
    name = repo + ' Open And Close Result'
    chart.set_title({'name': name})
    chart.set_x_axis({'name': 'Day'})
    chart.set_y_axis({'name': 'Count'})
    chart.set_style(10)

    addSeries('Open Critical', firstRow, startRow, 1, chart, sheetName)
    addSeries('Open High', firstRow, startRow, 2, chart, sheetName)
    addSeries('Open Medium', firstRow, startRow, 3, chart, sheetName)
    addSeries('Open Low', firstRow, startRow, 4, chart, sheetName)
    
    addSeries('Close Critical', firstRow, startRow, 5, chart, sheetName)
    addSeries('Close High', firstRow, startRow, 6, chart, sheetName)
    addSeries('Close Medium', firstRow, startRow, 7, chart, sheetName)
    addSeries('Close Low', firstRow, startRow, 8, chart, sheetName)

    insertCell = 'K' + str(firstRow + 1)
    worksheet.insert_chart(insertCell, chart, {"x_offset": 25, "y_offset": 10})
    return startRow


def addSeries(name, firstRow, startRow, col, chart, sheetName):
    chart.add_series({
        'name': name,
        'categories': [sheetName, firstRow + 3, 0, startRow - 1, 0],
        'values':     [sheetName, firstRow + 3, col, startRow - 1, col],
    })

def writeDetail(repo, workbook):
    print(f"Write Detail for {repo['repo']}")
    currentSheet = createSheet(workbook, repo['repo'])
    header = ['Number', 'State', 'Level', 'Create Date', 'Fixed Date', 'Dismiss Date', 'Dismiss By','Url', 'Dismiss Note']

    cell_format = workbook.add_format({
        'bold': True,
        'font_color': 'red',
        'bg_color': 'yellow',
        'border': 1
    })

    for i, value in enumerate(header):
        currentSheet.write(0, i, value, cell_format)
    currentSheet.set_column(0, 2, 10)
    currentSheet.set_column(3, 6, 20)
    currentSheet.set_column(7, 8, 75)

    contents = []
    for item in repo['items']:
        fixedDate = ''
        if item['fixedDate'] is not None:
            fixedDate = item['fixedDate'].strftime('%y-%m-%d %H:%M:%S')
        dismissDate = ''
        if item['dismissedDate'] is not None:
            dismissDate = item['dismissedDate'].strftime('%y-%m-%d %H:%M:%S')
        createDate = item['createDate'].strftime('%y-%m-%d %H:%M:%S')
        temp_row = [item['number'],item['state'],item['security_severity_level'], createDate, fixedDate, dismissDate, item['dismissedBy'] ,item['url'], item['dismissedReason']]
        contents.append(temp_row)
    for i, row in enumerate(contents, start=1):
        for j, value in enumerate(row):
            currentSheet.write(i, j, value)
