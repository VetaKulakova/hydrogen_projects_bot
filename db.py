import pandas as pd

with pd.ExcelFile("/Users/elizavetakulakova/Desktop/GAZPROM_CPS/Bots/namesbot/bots/hydrogen_projects_bot/Hydrogen_production_projects.xlsx") as xls:
    hydr_proj_data = pd.read_excel(xls, "data")
    
df = pd.DataFrame(hydr_proj_data, columns=['Project name', 'Country','Date online', 'Technology', 'Announced Size'])