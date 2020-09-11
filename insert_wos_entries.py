import csv
import pprint

from pathlib import Path

wos_header_map = {
    "FN": "File Name",
    "VR": "Version Number",
    "PT": "Publication",
    "AU": "Authors",
    "AF": "Author Full Name",
    "BA": "Book Authors",
    "BF": "Book Authors Full Name",
    "CA": "Group Authors",
    "GP": "Book Group Authors",
    "BE": "Editors",
    "TI": "Document Title",
    "SO": "Publication Name",
    "SE": "Book Series Title",
    "BS": "Book Series Subtitle",
    "LA": "Language",
    "DT": "Document Type",
    "CT": "Conference Title",
    "CY": "Conference Date",
    "CL": "Conference Location",
    "SP": "Conference Sponsors",
    "HO": "Conference Host",
    "DE": "Author Keywords",
    "ID": "Keywords Plus®",
    "AB": "Abstract",
    "C1": "Author Address",
    "RP": "Reprint Address",
    "EM": "E-mail Address",
    "RI": "ResearcherID Number",
    "OI": "ORCID",
    "FU": "Funding Agency and Grant Number",
    "FX": "Funding Text",
    "CR": "Cited References",
    "NR": "Cited Reference Count",
    "TC": "Web of Science Core Collection Times Cited Count",
    "Z9": "Total Times Cited Count (Web of Science Core Collection, Arabic Citation Index, BIOSIS Citation Index, Chinese Science Citation Database, Data Citation Index, Russian Science Citation Index, SciELO Citation Index)",
    "U1": "Usage Count (Last 180 Days)",
    "U2": "Usage Count (Since 2013)",
    "PU": "Publisher",
    "PI": "Publisher City",
    "PA": "Publisher Address",
    "SN": "International Standard Serial Number (ISSN)",
    "EI": "Electronic International Standard Serial Number (eISSN)",
    "BN": "International Standard Book Number (ISBN)",
    "J9": "29-Character Source Abbreviation",
    "JI": "ISO Source Abbreviation",
    "PD": "Publication Date",
    "PY": "Year Published",
    "VL": "Volume",
    "IS": "Issue",
    "SI": "Special Issue",
    "PN": "Part Number",
    "SU": "Supplement",
    "MA": "Meeting Abstract",
    "BP": "Beginning Page",
    "EP": "Ending Page",
    "AR": "Article Number",
    "DI": "Digital Object Identifier (DOI)",
    "D2": "Book Digital Object Identifier (DOI)",
    "EA": "Early access date",
    "EY": "Early access year",
    "PG": "Page Count",
    "P2": "Chapter Count (Book Citation Index)",
    "WC": "Web of Science Categories",
    "SC": "Research Areas",
    "GA": "Document Delivery Number",
    "PM": "PubMed ID",
    "UT": "Accession Number",
    "OA": "Open Access Indicator",
    "HP": "ESI Hot Paper. Note that this field is valued only for ESI subscribers.",
    "HC": "ESI Highly Cited Paper. Note that this field is valued only for ESI subscribers.",
    "DA": "Date this report was generated.",
    "ER": "End of Record",
    "EF": "End of File"
}


def get_wos_header_name(wos_header):
    if wos_header not in wos_header_map:
        raise ValueError

    return wos_header_map[wos_header]


def get_wos_entries(path):
    with open(path, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        headers = []
        for idx, row in enumerate(reader):
            if idx == 0:
                headers = row
            else:
                entry = {
                    get_wos_header_name(header): value 
                    for header, value in zip(headers, row)
                }

                pprint.pprint(entry)
         

if __name__ == "__main__":
    caltech_data = Path("data/caltech")
    files = [f for f in caltech_data.glob("**/*")]

    print(files)

    # test_path = "data/caltech/1-500.txt"
    # get_wos_entries(test_path)
