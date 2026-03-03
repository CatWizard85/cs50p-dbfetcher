import csv
from dbfread import DBF

def sanitize_field(value):
    if isinstance(value, str):
        # Sostituisci newline con spazio, puoi mettere ' | ' se vuoi dividerli meglio
        return value.replace('\r', ' ').replace('\n', ' ').strip()
    return value

def convert_dbf_to_csv_with_sanitized_desc(dbf_path, csv_path, exclude_columns=None, encoding='latin1'):
    if exclude_columns is None:
        exclude_columns = []

    table = DBF(dbf_path, encoding=encoding)
    field_names = [f for f in table.field_names if f not in exclude_columns]

    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=field_names, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for record in table:
            sanitized_record = {k: (sanitize_field(v) if k == "AA_DESCR2" else v) for k, v in record.items() if k in field_names}
            writer.writerow(sanitized_record)


convert_dbf_to_csv_with_sanitized_desc("ANAART.dbf", "ANAART.csv")


