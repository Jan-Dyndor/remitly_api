import pandas as pd
from database import engine
import os


if not os.path.exists("app/data/interns_2025_swift_codes.csv"):
    raise FileNotFoundError("CSV file not found in ./data/")

data = pd.read_csv("app/data/interns_2025_swift_codes.csv")
data = data.rename(
    columns={
        "SWIFT CODE": "swiftCode",
        "NAME": "bankName",
        "ADDRESS": "address",
        "COUNTRY ISO2 CODE": "countryISO2",
        "COUNTRY NAME": "countryName",
    }
)

data["isHeadquarter"] = data["swiftCode"].str.endswith("XXX")

needed_columns = [
    "countryISO2",
    "swiftCode",
    "bankName",
    "address",
    "countryName",
    "isHeadquarter",
]

relevant_data = data[needed_columns]
relevant_data
# Data in database will be replaced each time container runs!
# To change that use `append`
relevant_data.to_sql("swift_codes", con=engine, if_exists="replace", index=False)
