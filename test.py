import sys, os, csv, errno
import subprocess
from bs4 import BeautifulSoup, Tag

def readFile(filePath):
    if os.path.isfile(filePath):
        with open(filePath, 'r', encoding='UTF8') as f:
            reader = csv.reader(f, delimiter=':')
            content=[]
            for line in reader:
                content.append(line)
        return content
    else:
        raise FileNotFoundError(errno.ENOENT, 'File does not exist', filePath)

def generateHTMLReport(testData, output):
    testDataContent = readFile(testData)
    outputContent = readFile(output)

    htmlReportSoup = BeautifulSoup(features="html.parser")

    html = htmlReportSoup.new_tag('html')
    head = htmlReportSoup.new_tag('head')
    body = htmlReportSoup.new_tag('body')

    style =  htmlReportSoup.new_tag('style')
    h1 = htmlReportSoup.new_tag('h1')
    h3 = htmlReportSoup.new_tag('h3')
    
    htmlReportSoup.append(html)
    htmlReportSoup.html.append(head)
    htmlReportSoup.head.append(style)
    htmlReportSoup.style.string = '''
        table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding-left: 10px;
        }
    '''
    htmlReportSoup.html.append(body)
    htmlReportSoup.body.append(h1)
    htmlReportSoup.h1.string = 'REPORT'
    htmlReportSoup.body.append(h3)
    htmlReportSoup.h3.string = 'This report is automatically generated from running ugen.py program. Report shows results of proccessing test data from user selected data.'
    htmlReportSoup.body.append(htmlReportSoup.new_tag('table'))
    htmlReportSoup.table['style'] = "border: None; width: 100%;"
    htmlReportSoup.table.append(htmlReportSoup.new_tag('tr'))
    htmlReportSoup.tr.append(htmlReportSoup.new_tag('th'))
    htmlReportSoup.tr.append(htmlReportSoup.new_tag('th'))
    htmlReportSoup.find_all('th')[0]['style'] = "border: None; text-align: left;"
    htmlReportSoup.find_all('th')[1]['style'] = "border: None; text-align: left;"
    htmlReportSoup.find_all('th')[0].string = 'Test Data'
    htmlReportSoup.find_all('th')[1].string = 'Result'
    
    htmlReportSoup.table.append(htmlReportSoup.new_tag('tr'))
    htmlReportSoup.table.contents[1].append(htmlReportSoup.new_tag('td'))
    htmlReportSoup.table.contents[1].contents[0]['style'] = "border: None;"
    htmlReportSoup.table.contents[1].append(htmlReportSoup.new_tag('td'))
    htmlReportSoup.table.contents[1].contents[1]['style'] = "border: None;"
    
    #Test Data Table
    testDataNames = ['ID', 'Forename', 'Middle Name', 'Surname', 'Department']
    htmlReportSoup.table.contents[1].contents[0].append(htmlReportSoup.new_tag('table'))
    htmlReportSoup.table.contents[1].contents[0].contents[0]['style'] = "border: None;"
    htmlReportSoup.table.contents[1].contents[0].contents[0]['id'] = 'testDataTable'
    htmlReportSoup.find(id='testDataTable').append(htmlReportSoup.new_tag('tr'))

    for item in testDataNames:
        th = htmlReportSoup.new_tag('th')
        th.string = item
        htmlReportSoup.find(id='testDataTable').tr.append(th)
    
    for i, row in enumerate(testDataContent):
        htmlReportSoup.find(id='testDataTable').append(htmlReportSoup.new_tag('tr'))
        for cell in row:
            td = htmlReportSoup.new_tag('td')
            td.string = cell
            htmlReportSoup.find(id='testDataTable').contents[i+1].append(td)
    
    #Result Table
    resultNames = ['ID', 'Username', 'Forename', 'Middle Name', 'Surname', 'Department']
    htmlReportSoup.table.contents[1].contents[1].append(htmlReportSoup.new_tag('table'))
    htmlReportSoup.table.contents[1].contents[1].contents[0]['style'] = "border: None;"
    htmlReportSoup.table.contents[1].contents[1].contents[0]['id'] = 'resultTable'
    htmlReportSoup.find(id='resultTable').append(htmlReportSoup.new_tag('tr'))
    
    for item in resultNames:
        th = htmlReportSoup.new_tag('th')
        th.string = item
        htmlReportSoup.find(id='resultTable').tr.append(th)
    
    hasIncorrectValue = False
    incorrectValueRowCounter = 0
    for i, row in enumerate(outputContent):
        htmlReportSoup.find(id='resultTable').append(htmlReportSoup.new_tag('tr'))
        for cell in row:
            td = htmlReportSoup.new_tag('td')
            td.string = cell
            htmlReportSoup.find(id='resultTable').contents[i+1].append(td)
            if td.string == 'IncorrectValue':
                td['style'] = 'background-color:red'
        if htmlReportSoup.find(id='resultTable').contents[i+1].contents[1].string == '':
            htmlReportSoup.find(id='resultTable').contents[i+1].contents[1]['style'] = 'background-color:yellow;'
        if 'IncorrectValue' in row:
            hasIncorrectValue = True
            incorrectValueRowCounter +=1

    if not hasIncorrectValue:
        htmlReportSoup.body.append(htmlReportSoup.new_tag('h3'))
        htmlReportSoup.body.find_all('h3')[1].string = 'Usernames were generated successfully!'
        htmlReportSoup.body.find_all('h3')[1]['style'] = 'background-color:green;'
    
        p1 = htmlReportSoup.new_tag('p')
        p1.string = 'Test Data contains ' + str(len(outputContent)) + ' rows.'
        htmlReportSoup.body.append(p1)
    else:
        htmlReportSoup.body.append(htmlReportSoup.new_tag('h3'))
        htmlReportSoup.body.find_all('h3')[1].string = 'Usernames were not generated for all users!'
        htmlReportSoup.body.find_all('h3')[1]['style'] = 'background-color:red;'
        
        p1 = htmlReportSoup.new_tag('p')
        p1.string = 'Test Data contains ' + str(len(outputContent)) + ' rows.'
        p2 = htmlReportSoup.new_tag('p')
        p2.string = str(incorrectValueRowCounter) + ' rows contain incorrect values. Cells with incorrect values are highlighted in red.'
        p3 = htmlReportSoup.new_tag('p')
        p3.append('To generate username for missing users, please fix input data:')
        p3.append(htmlReportSoup.new_tag('br'))
        p3.append('ID should contain only numbers')
        p3.append(htmlReportSoup.new_tag('br'))
        p3.append('Forename, Middle Name, Surame and Department should contain only Letters and start with capital letter.')

        htmlReportSoup.body.append(p1)
        htmlReportSoup.body.append(p2)
        htmlReportSoup.body.append(p3)

    with open('report.html', 'w', encoding='UTF8') as f:
        f.write(str(htmlReportSoup))

def main(argv):
    ugen = argv[0]
    testData = argv[1]
    output = 'output.txt'
    subprocess.run('python ' + ugen + ' -o ' + output + ' ' + testData)
    generateHTMLReport(testData, output)

if __name__ == "__main__":
    main(sys.argv[1:])