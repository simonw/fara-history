from io import BytesIO, StringIO
from urllib.request import urlopen
import csv
import sqlite_utils

pks = {"FARA_All_Registrants": "Registration_Number"}

fts_columns = {
    "FARA_All_Registrants": ["Name", "Address_1", "Address_2"],
    "FARA_All_ForeignPrincipals": ["Foreign_Principal", "Registrant_Name"],
    "FARA_All_RegistrantDocs": [
        "Registrant_Name",
        "Short_Form_Name",
        "Foreign_Principal_Name",
    ],
    "FARA_All_ShortForms": [
        "Short_Form_Last_Name",
        "Short_Form_First_Name",
        "Registrant_Name",
    ],
}


def make_doc(data):
    new_data = {}
    for key, value in data.items():
        if "Date" in key and "/" in value:
            # Convert 06/11/2019 to yyyy-mm-dd
            mm, dd, yyyy = value.split("/")
            value = "{}-{}-{}".format(yyyy, mm, dd)
        # Registration_Number should be an integer
        if "Registration_Number" == key:
            if value.isdigit():
                value = int(value)
            else:
                print("Registration_Number is not numeric, skipping: ", data)
                return None
        new_data[key] = value
    return new_data


if __name__ == "__main__":
    db = sqlite_utils.Database("fara.db")
    for filename in (
        "FARA_All_Registrants.csv",
        "FARA_All_RegistrantDocs.csv",
        "FARA_All_ShortForms.csv",
        "FARA_All_ForeignPrincipals.csv",
    ):
        reader = csv.reader(open(filename))
        headers = [h.replace(" ", "_") for h in next(reader)]
        docs = (make_doc(dict(zip(headers, row))) for row in reader)
        table = filename.replace(".csv", "")
        # Using ignore=True because the CSVs contained a duplicate record
        db[table].insert_all((d for d in docs if d), pk=pks.get(table), ignore=True)
        # If any column is Registration_Number, set up foreign key
        if "Registration_Number" in headers:
            db[table].add_foreign_key("Registration_Number", "FARA_All_Registrants")
        # Set up FTS
        if table in fts_columns:
            db[table].enable_fts(fts_columns[table])
