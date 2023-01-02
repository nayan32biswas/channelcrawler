import csv
from datetime import datetime
import os
import requests
import xlsxwriter

from bs4 import BeautifulSoup

client = requests.Session()


def extract_content(content):
    results = []
    bs_content = BeautifulSoup(content, "html.parser")
    for div in bs_content.find_all(
        "div", {"class": "channel col-xs-12 col-sm-4 col-lg-3"}
    ):
        try:
            a = div.find("a")
            img = div.find("img")

            country = img["title"]
            name = a.contents[0] if a.contents else ""
            url = a["href"]

            results.append((country, name, url))
        except Exception as e:
            print(e)
    return results


def main():
    path = input("Enter file path: ").strip()

    results = [
        ["Country", "Channel name", "URL"],
    ]
    for filename in os.listdir(path):
        if filename.endswith(".html"):
            with open(os.path.join(path, filename), "r") as file:
                page_result = extract_content(file.read())
                for each in page_result:
                    results.append(each)

    root_folder = "xlsx"
    file_name = f"""{root_folder}/{datetime.utcnow().strftime("%Y%m%d--%H%M%S")}.xlsx"""

    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    for idx, data in enumerate(results):
        worksheet.write(idx + 1, *data)
    workbook.close()

    print(f"All data saved to {file_name}")


if __name__ == "__main__":
    main()
