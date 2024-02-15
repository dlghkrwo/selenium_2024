import openpyxl

#create excel file
xlsxFile = openpyxl.Workbook()

#create sheet from the file
xlsxSheet = xlsxFile.active

#input data into cells
xlsxSheet.cell(row = 1, colume = 1).value = "hi"
#find_element().txt로 찾은 값을 넣으면 됨

#save
xlsxFile.save('result.xlsx')
