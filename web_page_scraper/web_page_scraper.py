import requests
import string
import sys
from bs4 import BeautifulSoup
from pathlib import Path
from requests.exceptions import RequestException


class NatureParser:
    def __init__(self, pages_limit, article_type):
        self.limit = pages_limit
        self.target_kind = article_type
        self.base_link = "https://www.nature.com/nature/articles"
        self.session = requests.Session()
        # Кастомный заголовок браузера
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml"
        })

    def _sanitize_filename(self, title):
        """Превращает заголовок статьи в допустимое имя файла."""
        allowed = f"-() {string.ascii_letters}{string.digits}"
        name = ''.join(char for char in title if char in allowed)
        return name.strip().replace(" ", "_")[:100]

    def _get_request(self, url, params=None):
        """Вспомогательный метод для сетевых запросов."""
        try:
            response = self.session.get(url, params=params, timeout=20)
            response.raise_for_status()
            return response
        except RequestException as e:
            print(f"Ошибка соединения с {url}: {e}")
            return None

    def _parse_article_text(self, url):
        """Извлекает текст статьи из найденной страницы."""
        req = self._get_request(url)
        if not req:
            return None

        page_data = BeautifulSoup(req.text, "html.parser")

        # Различные варианты верстки для поиска текста
        content_selectors = [
            "article.c-article-body",
            "div.article-item__body",
            "div[itemprop='articleBody']",
            "section[data-test='article-body']"
        ]

        for selector in content_selectors:
            box = page_data.select_one(selector)
            if box:
                paragraphs = box.find_all("p")
                text = "\n".join(p.get_text().strip() for p in paragraphs)
                if text:
                    return text

        # Если основной блок не найден, ищем анонс
        teaser = page_data.find("p", class_="article__teaser")
        return teaser.get_text() if teaser else None

    def _process_page(self, num):
        print(f"--- Обработка раздела №{num} ---")

        parameters = {
            "year": "2022",
            "sort": "PubDate",
            "page": num
        }

        resp = self._get_request(self.base_link, params=parameters)
        if not resp:
            return

        web_soup = BeautifulSoup(resp.text, "html.parser")

        # Подготовка папки для текущей страницы
        folder = Path(f"Page_{num}")
        folder.mkdir(exist_ok=True)

        cards = web_soup.find_all("article")
        if not cards:
            print(f"Статьи на странице {num} не обнаружены.")
            return

        for card in cards:
            # Сверяем тип публикации
            meta = card.find("span", {"data-test": "article.type"})
            if not meta or meta.get_text().strip() != self.target_kind:
                continue

            anchor = card.find("a", {"data-track-action": "view article"})
            if not anchor:
                continue

            header_text = anchor.get_text().strip()
            web_path = anchor.get("href")
            full_url = f"https://www.nature.com{web_path}"

            print(f"Загружаю: {header_text[:40]}...")

            article_content = self._parse_article_text(full_url)
            if not article_content:
                continue

            safe_name = self._sanitize_filename(header_text) + ".txt"
            file_path = folder / safe_name

            try:
                file_path.write_text(article_content, encoding="utf-8")
            except IOError as io_err:
                print(f"Не удалось сохранить файл {safe_name}: {io_err}")

    def run(self):
        for page_idx in range(1, self.limit + 1):
            self._process_page(page_idx)
        print("\nГотово. Все доступные материалы скачаны.")


def main():
    while True:
        try:
            total_pages = int(input("Укажите число страниц для парсинга: "))
            if total_pages > 0:
                break
        except ValueError:
            pass
        print("Пожалуйста, введите корректное число.")

    wanted_type = input("Какую категорию ищем? (например, Research Highlight): ").strip()

    scanner = NatureParser(total_pages, wanted_type)
    scanner.run()


if __name__ == "__main__":
    main()