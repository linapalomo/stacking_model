import json
import pandas as pd
##print initial distribution in a datafram for better view, anaylisis 

with open("data.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Set pandas to show all rows and columns
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
print(df)
