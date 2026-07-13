import argparse
import urllib.request, urllib.error
from bs4 import BeautifulSoup

def extract_images(url: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all('img'):
        print(link.get("src"))

def fetch_page(url : str):
    try:
        with urllib.request.urlopen(url, timeout = 10) as response:
            html = response.read().decode()
        return html
    except ValueError:
        print("Url format invalid")
        return None
    except urllib.error.HTTPError:
        print("Error HTTP")
        return None
    except urllib.error.URLError:
        print("Url error")
        return None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url from the website you want to extract images")
    parser.add_argument("-r", help="recursively downloads the images", action="store_true")
    parser.add_argument("-l", "--level", type=int, default=None)
    parser.add_argument("-p", "--path", type=str, default="./data/")
    args = parser.parse_args()
    if args.level is not None and not args.r:
        parser.error("-l need to be used with -r")
    elif args.r and args.level is None:
        args.level = 5
    return args


def spider():
    args = parse_args()
    #html = fetch_page(args.url)
    html = open("test_page.html").read()
    #print(html)
    extract_images(args.url, html)



if __name__ == "__main__":
    spider()
