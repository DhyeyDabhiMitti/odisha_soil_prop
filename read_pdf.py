import pdfplumber
import pandas as pd


table1_lst = []
table2_lst = []

with pdfplumber.open('Soil Series of Orissa.pdf') as pdf:
    j=19
    for i,page in enumerate(pdf.pages):
        if i==j and i<255:
            tables = page.extract_tables()
            if len(tables)==0:
                j+=1
                continue
            temp_table = tables[-2]
            for row in temp_table:
                row.append(i)
            table1_lst.append(temp_table)
            j+=2

dfs = [pd.DataFrame(table) for table in table1_lst]
combined_df = pd.concat(dfs,ignore_index=True)
combined_df.to_csv('new_table.csv')

