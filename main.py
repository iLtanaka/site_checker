import argparse
import requests
import string
import itertools
import time
import os
from bs4 import BeautifulSoup

def generate_links(characters, length):
    for chars in itertools.product(characters, repeat=length):
        yield ''.join(chars)

def check_link(base_url, subdomain):
    url = f"https://{subdomain}.{base_url}/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            title = extract_title(response.text)
            return True, title  
        elif response.status_code == 404:
            return False, None  
        else:
            return False, None  
    except requests.RequestException as e:
        print(f"Ошибка запроса для URL")
        return False, None  

def extract_title(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "Нет заголовка"
        return title.strip()
    except Exception as e:
        return f"Ошибка при извлечении заголовка: {e}"

def main():
    parser = argparse.ArgumentParser(description="Скрипт для проверки субдоменов и извлечения заголовков.")
    parser.add_argument(
        "--base-url",
        type=str,
        default="narod.ru",
        help="Базовый URL для проверки субдоменов (по умолчанию: narod.ru)"
    )
    args = parser.parse_args()

    base_url = args.base_url
    characters = string.ascii_lowercase + string.digits
    progress_file = "progress.txt"
    output_file = "working_links_with_titles.txt"

    current_length = 1
    start_from = None
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            data = f.read().strip().split(":")
            current_length = int(data[0])
            start_from = data[1] if len(data) > 1 else None

    while True:
        print(f"\nНачало проверки для длины {current_length}")
        found = False
        for subdomain in generate_links(characters, current_length):
            if start_from and not found:
                if subdomain == start_from:
                    found = True
                continue
            found = True

            print(f"Проверка: https://{subdomain}.{base_url}/")
            is_working, title = check_link(base_url, subdomain)
            if is_working:
                print(f"[+] Найдена рабочая ссылка: https://{subdomain}.{base_url}/, Заголовок: {title}")
                with open(output_file, "a") as f:
                    f.write(f"https://{subdomain}.{base_url}/ - {title}\n")
            else:
                print(f"[-] Ссылка не найдена: https://{subdomain}.{base_url}/")

            with open(progress_file, "w") as f:
                f.write(f"{current_length}:{subdomain}")

        print(f"Проверка для длины {current_length} завершена.")
        current_length += 1
        start_from = None

if __name__ == "__main__":
    main()