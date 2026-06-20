from bs4 import BeautifulSoup
from os import makedirs
from os.path import isdir
from urllib.parse import urljoin
import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

session = requests.Session()

def createdir(path):
    if not isdir(path):
        makedirs(path)

def make_safe_filename(s):
    return "".join(c if c.isalnum() else "_" for c in s).rstrip("_")

def download_file(url, path, num):
    filename = f"{path}/Photo-{num}.jpg"

    try:
        r = session.get(url, timeout=30)

        if r.status_code == 200 and "image" in r.headers.get("Content-Type", ""):
            with open(filename, "wb") as file:
                file.write(r.content)

            print(f"OK [{num}] -> {filename}")
            return True

        print(f"ERROR [{num}] -> {r.status_code} {r.headers.get('Content-Type')}")
        return False

    except Exception as e:
        print(f"ERROR descargando foto {num}: {e}")
        return False

def get_big_image(photo_url):
    try:
        r = session.get(photo_url, timeout=30)
        soup = BeautifulSoup(r.content, "html.parser")

        meta = soup.find("meta", {"property": "og:image"})

        if not meta:
            print(f"No encuentro og:image en {photo_url}")
            return None

        img = meta["content"]
        img = img.replace("4.jpg", "5.jpg")

        return img

    except Exception as e:
        print(f"ERROR leyendo página de foto: {e}")
        return None

def get_all_photo_links_with_selenium(album_url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,3000")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(album_url)
        time.sleep(3)

        last_count = 0
        same_count_times = 0

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            elements = driver.find_elements(By.CSS_SELECTOR, "a.pv-inner")
            current_count = len(elements)

            print(f"Miniaturas cargadas: {current_count}")

            if current_count == last_count:
                same_count_times += 1
            else:
                same_count_times = 0

            if same_count_times >= 3:
                break

            last_count = current_count

        soup = BeautifulSoup(driver.page_source, "html.parser")

        links = []

        for a in soup.find_all("a", class_=lambda c: c and "pv-inner" in c):
            href = a.get("href")

            if href:
                full_url = urljoin(album_url, href)

                if full_url not in links:
                    links.append(full_url)

        return links, soup

    finally:
        driver.quit()

def download_zenfolio_album(album_url):
    print("Fetching album metadata with Selenium...")

    links, soup = get_all_photo_links_with_selenium(album_url)

    title_tag = soup.find("span", {"class": "title breadcrumbs-font3"})

    if title_tag:
        album_title = make_safe_filename(title_tag.text)
    else:
        album_title = "zenfolio_album"

    print(f"Álbum: {album_title}")
    print(f"Fotos encontradas: {len(links)}")

    createdir(album_title)

    descargadas = 0
    errores = 0

    for i, photo_page in enumerate(links, start=1):
        print(f"\n[{i}/{len(links)}] {photo_page}")

        img_url = get_big_image(photo_page)

        if not img_url:
            errores += 1
            continue

        if download_file(img_url, album_title, i):
            descargadas += 1
        else:
            errores += 1

        time.sleep(0.5)

    print("\n======================")
    print(f"Descargadas: {descargadas}")
    print(f"Errores: {errores}")
    print("======================")

print("Zenfolio Album Downloader")
print("=" * 30)

album_url = input("Introduce la URL del álbum: ").strip()
download_zenfolio_album(album_url)