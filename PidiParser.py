import pandas as pd
import re
importedData = pd.read_excel(r'C:\Users\JiriZ\Downloads\brc2-mapa-191213.xlsx', sheet_name='navrh Fatek').iloc[9:,2:4].dropna().reset_index(drop=True).values.tolist()
BrcRegisterNumbers = []
BrcRegisterBitNumbers = []
for row in importedData:
    if "." not in row[0]:
        BrcRegisterNumbers.append("\t" + re.sub(r' ', '_',(row[0] + "_" + row[1])) + " = " + row[0] + ",\n")
    else:
        BrcRegisterBitNumbers.append("\t" + re.sub(r' ', '_', (row[0] + "_" + row[1])) + " = " + bin(int(re.sub(r'.*\.', '', row[0]))) + ",\n")
registers = open("registers.h","w+")
registers.write("struct BrcRegisterNumbers {enum Enum {\n")
registers.writelines(BrcRegisterNumbers)
registers.write("};};\n\n")
registers.write("struct BrcRegisterBitNumbers {enum Enum {\n")
registers.writelines(BrcRegisterBitNumbers)
registers.write("};};")
registers.close()