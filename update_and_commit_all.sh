#!/bin/bash
fetch_and_sort () {
    # $1 is the table name, $2 is the URL
    local table=$1
    local zip_url=$2
    local zip="$1.csv.zip"
    local csv="$1.csv"
    local csv_unsorted="$1.csv.unsorted"
    local csv_old="$1.csv.old"
    local commit_txt="$1.commit.txt"
    mv $csv $csv_old
    curl -s -o $zip $2
    unzip -q -o $zip
    # This should have created the .csv file
    mv $csv $csv_unsorted
    # Construct new CSV with heading line + sorted other lines
    head -n 1 $csv_unsorted | tr ' ' '_' > $csv
    tail -n +2 $csv_unsorted | sort >> $csv
    echo "Updated $csv" > $commit_txt
    echo $'\n[skip ci]' >> $commit_txt
}

fetch_and_diff () {
    fetch_and_sort $1 $2
    local csv_diff_args=$3
    local csv="$1.csv"
    local csv_old="$1.csv.old"
    local commit_txt="$1.commit.txt"
    csv-diff $csv_old $csv $csv_diff_args > $commit_txt
    echo $'\n[skip ci]' >> $commit_txt
}

add_and_commit () {
    local csv="$1.csv"
    local commit_txt="$1.commit.txt"
    git add $csv
    git commit -F $commit_txt && \
        git push -q origin master \
        || true
}

git config --global user.email "farabot@example.com"
git config --global user.name "Farabot"

fetch_and_diff FARA_All_Registrants "https://efile.fara.gov/bulk/zip/FARA_All_Registrants.csv.zip" "--key=Registration_Number"
add_and_commit FARA_All_Registrants
fetch_and_sort FARA_All_RegistrantDocs "https://efile.fara.gov/bulk/zip/FARA_All_RegistrantDocs.csv.zip"
add_and_commit FARA_All_RegistrantDocs
fetch_and_sort FARA_All_ShortForms "https://efile.fara.gov/bulk/zip/FARA_All_ShortForms.csv.zip"
add_and_commit FARA_All_ShortForms
fetch_and_sort FARA_All_ForeignPrincipals "https://efile.fara.gov/bulk/zip/FARA_All_ForeignPrincipals.csv.zip"
add_and_commit FARA_All_ForeignPrincipals
