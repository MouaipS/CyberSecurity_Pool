import argparse
import urllib.request
import ssl
import urllib.error
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse


VALID_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


def setup_https() -> None:
    """Configure un opener global avec un contexte SSL par défaut,
    utilisé automatiquement par urlopen ET urlretrieve."""
    context = ssl.create_default_context()
    https_handler = urllib.request.HTTPSHandler(context=context)
    opener = urllib.request.build_opener(https_handler)
    opener.addheaders = [
        ("User-Agent", "Mozilla/5.0")
    ]
    urllib.request.install_opener(opener)


def download_image(url: str, path: str) -> None:
    os.makedirs(path, exist_ok=True)
    filename = os.path.basename(urlparse(url).path)
    if not filename:
        return
    filepath = os.path.join(path, filename)
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded: {filename}")
    except (urllib.error.HTTPError, urllib.error.URLError, ssl.SSLError) as e:
        print(f"Failed to download {url}: {e}")


def is_valid_image(url: str) -> bool:
    clean = url.split("?")[0].split("#")[0]
    return clean.lower().endswith(VALID_EXT)


def is_valid_url(url_target: str, url: str) -> bool:
    if urlparse(url_target).netloc !=  urlparse(url).netloc:
        return False
    return True


def extract_images(url: str, html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    src_list = []
    for link in soup.find_all('img'):
        src = link.get("src")
        if src is None or src.startswith("data:"):
            continue
        absolute_url = urljoin(url, src)
        if is_valid_image(absolute_url):
            src_list.append(absolute_url)
    return set(src_list)


def extract_links(url: str, html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    src_list = []
    for link in soup.find_all('a'):
        src = link.get("href")
        if src is None or src.startswith(("#", "mailto:", "tel:")):
            continue
        absolute_url = urljoin(url, src)
        if is_valid_image(absolute_url):
            continue
        if is_valid_url(absolute_url, url):
            src_list.append(absolute_url)
    return set(src_list)


def fetch_page(url: str):
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            html = response.read().decode()
        return html
    except ssl.SSLError:
        print("Erreur SSL : certificat invalide ou connexion non sécurisée")
        return None
    except ValueError:
        print("Url format invalid")
        return None
    except urllib.error.HTTPError as e:
        print(f"Error HTTP: {e.code} {e.reason}")
        return None
    except urllib.error.URLError:
        print("Url error")
        return None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url of the website to extract images")
    parser.add_argument("-r", help="recursively deep", action="store_true")
    parser.add_argument("-l", "--level", type=int, default=None)
    parser.add_argument("-p", "--path", type=str, default="./data/")
    args = parser.parse_args()
    if args.level is not None and not args.r:
        parser.error("-l need to be used with -r")
    elif args.r and args.level is None:
        args.level = 5
    return args


def spider():
    #setup_https()
    args = parse_args()
    #html = fetch_page(args.url)
    #if html is None:
        #return
    html = open("test_page.html").read()
    images = extract_images("http://example.com/test_page.html", html)
    print(images)

    links = extract_links("http://example.com/test_page.html", html)
    print(links)

    #for elem in images:
    #    download_image(elem, args.path)


if __name__ == "__main__":
    spider()
