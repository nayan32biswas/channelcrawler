import csv
from datetime import datetime
import os
import requests

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

    root_folder = "csv"
    file_name = f"""{root_folder}/{datetime.utcnow().strftime("%Y%m%d--%H%M%S")}.csv"""

    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    with open(file_name, "w", newline="") as csvfile:
        my_writer = csv.writer(csvfile, delimiter=" ")
        my_writer.writerows(results)
    print(f"All data saved to {file_name}")


if __name__ == "__main__":
    main()
