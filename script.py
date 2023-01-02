import csv
from datetime import datetime
import os
import requests

from bs4 import BeautifulSoup

client = requests.Session()


def extract_content(content):
    results = []
    bs_content = BeautifulSoup(content, "html.parser", from_encoding="iso-8859-1")
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


def get_content(url=""):
    response = client.post(url)

    if response.status_code == 200:
        print("")
        results = extract_content(response.content)
        print(f"URL:{url} data loaded successfully")
        return results
    else:
        print(f"Something wrong with url with status code {response.status_code}.")

    return False


def set_auth():
    """
    data[User][username]: <email>
    data[User][password]: <password>
    """
    login_information = {
        "User.username": "sabu.prof@gmail.com",
        "User.password": "halalz123",
    }

    client.post("https://channelcrawler.com/users/login", data=login_information)


def main():
    # https://channelcrawler.com/eng/results2/1854021
    base_url = input("Url: ").strip()
    page_size = input("Maximum page (default 1M): ")
    max_page = 2
    try:
        max_page = int(page_size)
    except Exception:
        pass

    print("Authenticating.")
    set_auth()
    print("authentication complete")

    results = [
        ["Country", "Channel name", "URL"],
    ]
    idx = 1
    while idx <= max_page:
        url = base_url + f"/page:{idx}" if idx > 1 else base_url
        page_result = get_content(url)
        if page_result:
            results.append(["Page", url])
            for each in page_result:
                results.append(each)
        else:
            print(f"raise error to get data for ULR {url}")
            text = input("Do you read this page again?(no/yes): ")
            if "no" in text:
                break
            else:
                idx -= 1
        idx += 1

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
