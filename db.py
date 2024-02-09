import pandas as pd
from links import PATH_TO_DATASET

with pd.ExcelFile(PATH_TO_DATASET) as xls:
    hydr_proj_data = pd.read_excel(xls, "data")

df = pd.DataFrame(hydr_proj_data, columns=['Project name', 'Country',
                                           'Date online', 'Technology',
                                           'Announced Size'])
