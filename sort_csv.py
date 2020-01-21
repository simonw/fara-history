"Script to output a CSV file with the rows sorted alphabetically"
import csv
import sys


def sort_csv(filename, outfile=sys.stdout, underscores_in_headers=True):
    reader = csv.reader(open(filename))
    headers = next(reader)
    if underscores_in_headers:
        headers = [h.replace(" ", "_") for h in headers]
    # Load all rows, then sort them
    rows = [r for r in reader]
    rows.sort(key=repr)
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
    writer.writerow(headers)
    writer.writerows(rows)


if __name__ == "__main__":
    filepath = sys.argv[-1]
    sort_csv(filepath)
