# main.py

from util.utils import summarizeIssue, calTotal, calAllTotal
from query.codeql import loadIssue
from util.excelutils import createFile, createSheet, writeSummary, saveFile, writeDetail, writeTotal

def main():
    repos = ['a1-app-orms', 'a1-app-ormsui', 'a1-app-licensing', 'a1-app-uwp', 'a1-app-ormsreports', 'a1-app-config', 'a1-app-cmty']
    #repos = ['a1-app-ormsui', 'a1-app-config']
    allSummary = []
    repoIssues = loadIssue(repos)

    workbook = createFile()
    sheetName = 'Summary'
    summarySheet = createSheet(workbook, sheetName)

    startRow = 0
    for repoIssue in repoIssues:
        summary = summarizeIssue(repoIssue['items'])
        allSummary.append(summary)
        startRow = writeSummary(workbook, summarySheet, summary, repoIssue['repo'], startRow, sheetName)
        writeDetail(repoIssue, workbook)
        startRow = startRow + 2

    totalSummary = calTotal(allSummary)
    startRow = writeSummary(workbook, summarySheet, totalSummary, 'Total', startRow, sheetName)
    startRow = startRow + 2

    totalCount = calAllTotal(repoIssues)
    writeTotal(workbook, summarySheet, totalCount, 'Open/Close/Total for Repo', startRow)
    saveFile(workbook)

if __name__ == "__main__":
    main()