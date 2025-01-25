from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib
import json
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
sys.stdout.reconfigure(encoding='utf-8')

# AFAIK this is not needed for latest version of selenium
DRIVER_PATH = "c/Users/szymo/PROGRAMMING/geckodriver-v0.35.0-win64"


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):

    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # Google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    wd.get(search_url.format(q=query))
    print("Searching for:", query)

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:

        if image_count > 30:
            break

        scroll_to_end(wd)

        # Get all images thumbnail results
        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} results.")
        
        for thumbnail in thumbnail_results[results_start:number_results]:
            try:
                thumbnail.click()
                WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.sFlh5c.FyHeAf.iPVvYb')))
            except Exception:
                continue

            # Get image urls by css selector 
            actual_images = wd.find_elements(By.CSS_SELECTOR, 'img.sFlh5c.FyHeAf.iPVvYb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break


        if results_start >= number_results:
            print("No more new thumbnails found, breaking the loop.")
            break

        results_start = len(thumbnail_results)

    return image_urls

def download_image(folder_path:str, file_name:str, url:str):

    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Img url {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


if __name__ == '__main__':
    options = webdriver.FirefoxOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    

    outpud_dir = 'selenium_image_folders'
    os.makedirs(outpud_dir, exist_ok=True)
    
    input_json_file = "stop_motion/filtered_folders.json"

    with open(input_json_file, 'r', encoding='utf-8') as file:
        movies = json.load(file)
    
    queries = [ entry["movie_title"] for entry in movies]
    

    for query in queries[55:]:
        wd = webdriver.Firefox(options=options)
        wd.get('https://google.com')
        accept_button = WebDriverWait(wd, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Zaakceptuj wszystko']"))
            )
        accept_button.click()

        links = fetch_image_urls(("stop motion movie " + query), 30 ,wd)

        for i in links:
            download_image(outpud_dir, query,i)

        wd.quit()