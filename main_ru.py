import argparse
import asyncio
import aiohttp
import string
import itertools
import os
from bs4 import BeautifulSoup

def generate_links(characters, length):
    for chars in itertools.product(characters, repeat=length):
        yield ''.join(chars)

async def check_link(session, base_url, subdomain):
    url = f"https://{subdomain}.{base_url}/"
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                html = await response.text()
                title = extract_title(html)
                return url, title
            return None, None
    except Exception:
        return None, None

def extract_title(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "Нет заголовка"
        return title.strip()
    except Exception:
        return "Ошибка при извлечении заголовка"

async def main():
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

    async with aiohttp.ClientSession() as session:
        while True:
            print(f"\nНачало проверки для длины {current_length}")
            found = False
            tasks = []

            for subdomain in generate_links(characters, current_length):
                if start_from and not found:
                    if subdomain == start_from:
                        found = True
                    continue
                found = True

                tasks.append(check_link(session, base_url, subdomain))

                if len(tasks) >= 100:
                    results = await asyncio.gather(*tasks)
                    for url, title in results:
                        if url:
                            print(f"[+] Найдена рабочая ссылка: {url}, Заголовок: {title}")
                            with open(output_file, "a") as f:
                                f.write(f"{url} - {title}\n")
                    tasks = []

            results = await asyncio.gather(*tasks)
            for url, title in results:
                if url:
                    print(f"[+] Найдена рабочая ссылка: {url}, Заголовок: {title}")
                    with open(output_file, "a") as f:
                        f.write(f"{url} - {title}\n")

            print(f"Проверка для длины {current_length} завершена.")
            current_length += 1
            start_from = None

if __name__ == "__main__":
    asyncio.run(main())