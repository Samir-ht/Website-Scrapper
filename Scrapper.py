# import requests
# from bs4 import BeautifulSoup
# import os
# import time
# import shutil
# from urllib.parse import urljoin, urlparse
#
#
# class WebsiteScraper:
#     def __init__(self, base_url, delay=1):
#         self.base_url = base_url
#         self.domain = urlparse(base_url).netloc
#         self.visited = set()
#         self.delay = delay
#         self.output_base = "scraped_site_files"
#         # Statistics for the comparison log
#         self.stats = {
#             "total_routes_found": 0,
#             "successful_scrapes": 0,
#             "failed_scrapes": 0,
#             "start_time": time.time()
#         }
#
#     def get_local_path(self, url):
#         parsed = urlparse(url)
#         path = parsed.path
#         if not path or path == "/":
#             path = "/index"
#
#         parts = path.strip("/").split("/")
#         local_dir = os.path.join(self.output_base, *parts[:-1]) if len(parts) > 1 else self.output_base
#
#         if not os.path.exists(local_dir):
#             os.makedirs(local_dir)
#
#         return os.path.join(local_dir, f"{parts[-1]}.txt")
#
#     def scrape_site(self, current_url):
#         if current_url in self.visited or self.domain not in current_url:
#             return
#
#         self.stats["total_routes_found"] += 1
#         print(f"[{self.stats['total_routes_found']}] Scraping: {current_url}")
#         self.visited.add(current_url)
#
#         try:
#             time.sleep(self.delay)
#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
#             response = requests.get(current_url, headers=headers, timeout=10)
#
#             if response.status_code == 200:
#                 self.stats["successful_scrapes"] += 1
#                 soup = BeautifulSoup(response.text, 'html.parser')
#
#                 # Content extraction logic
#                 main_content = soup.find('main') or soup.find('article') or soup.body
#                 clean_text = main_content.get_text(separator='\n', strip=True)
#
#                 with open(self.get_local_path(current_url), "w", encoding="utf-8") as f:
#                     f.write(f"URL: {current_url}\n{clean_text}")
#
#                 # Find internal links
#                 for link in soup.find_all('a', href=True):
#                     full_url = urljoin(self.base_url, link['href']).split('#')[0].rstrip('/')
#                     self.scrape_site(full_url)
#             else:
#                 self.stats["failed_scrapes"] += 1
#         except Exception:
#             self.stats["failed_scrapes"] += 1
#
#     def print_summary(self):
#         end_time = time.time()
#         duration = round(end_time - self.stats["start_time"], 2)
#
#         print("\n" + "=" * 40)
#         print("📊 SCRAPING SUMMARY LOG")
#         print("=" * 40)
#         print(f"Total Routes Discovered: {self.stats['total_routes_found']}")
#         print(f"Successfully Saved:     {self.stats['successful_scrapes']} files")
#         print(f"Failed/Skipped:          {self.stats['failed_scrapes']}")
#         print(f"Total Time Taken:        {duration} seconds")
#         print("=" * 40)
#
#     def create_zip(self):
#         shutil.make_archive("scraped_data_package", 'zip', self.output_base)
#         print("\n✅ ZIP file created successfully.")
#
#
# if __name__ == "__main__":
#     target = "https://www.hashtechy.com/"  # Change this
#     bot = WebsiteScraper(target, delay=0.5)
#     try:
#         bot.scrape_site(target)
#     finally:
#         bot.print_summary()  # Shows the log before finishing
#         bot.create_zip()
import requests
from bs4 import BeautifulSoup
import os
import time
import shutil
from urllib.parse import urljoin, urlparse


class VectorReadyScraper:
    def __init__(self, base_url, delay=0.5):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.delay = delay
        self.output_base = "formatted_texts"
        self.stats = {"count": 0}

        if not os.path.exists(self.output_base):
            os.makedirs(self.output_base)

    # def format_content(self, soup):
    #     """
    #     Organizes text by finding headers and the specific
    #     paragraphs that follow them.
    #     """
    #     formatted_output = []
    #
    #     # 1. Focus only on the main content area to avoid nav/footer noise
    #     container = soup.find('main') or soup.find('article') or soup.body
    #
    #     # 2. Find all relevant structural tags in the order they appear
    #     # This is the secret to the "Header > Content" format
    #     elements = container.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li'])
    #
    #     for el in elements:
    #         text = el.get_text(strip=True)
    #         if not text:
    #             continue
    #
    #         if el.name in ['h1', 'h2', 'h3', 'h4']:
    #             # Label headers clearly
    #             formatted_output.append(f"\n[HEADER: {text.upper()}]")
    #         elif el.name == 'li':
    #             # Format list items with a bullet
    #             formatted_output.append(f"  • {text}")
    #         else:
    #             # Regular paragraph content
    #             formatted_output.append(text)
    #
    #     return "\n".join(formatted_output)
    def format_content(self, soup):
        """
        Organizes text by finding headers and the specific
        paragraphs that follow them, excluding header/footer.
        """
        formatted_output = []

        # 1. Focus only on the main content area
        container = soup.find('main') or soup.find('article') or soup.body
        if not container:
            return ""

        # 2. REMOVE unwanted layout elements
        for tag in container.find_all(
                ['header', 'footer', 'nav', 'aside', 'form', 'script', 'style']
        ):
            tag.decompose()

        # 3. Extract content in visual order
        elements = container.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li'])

        for el in elements:
            text = el.get_text(strip=True)
            if not text:
                continue

            if el.name in ['h1', 'h2', 'h3', 'h4']:
                formatted_output.append(f"\n[HEADER: {text.upper()}]")
            elif el.name == 'li':
                formatted_output.append(f"  • {text}")
            else:
                formatted_output.append(text)

        return "\n".join(formatted_output)

    def scrape_site(self, current_url):
        # Clean the URL to avoid duplicates
        normalized_url = current_url.split('#')[0].rstrip('/')
        if normalized_url in self.visited or self.domain not in current_url:
            return

        self.visited.add(normalized_url)
        self.stats["count"] += 1
        print(f"Scraping [{self.stats['count']}]: {normalized_url}")

        try:
            time.sleep(self.delay)
            # headers = {'User-Agent': 'Mozilla/5.0'}
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Connection": "keep-alive",
            }
            response = requests.get(current_url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Get the formatted body text
                body_text = self.format_content(soup)

                # Construct the final file string
                final_text = (
                    f"SOURCE: {normalized_url}\n"
                    f"TITLE: {soup.title.string if soup.title else 'No Title'}\n"
                    f"{'=' * 50}\n"
                    f"{body_text}"
                )

                # Save as .txt
                safe_name = "".join([c if c.isalnum() else "_" for c in urlparse(current_url).path])
                if not safe_name or safe_name == "_": safe_name = "index"

                filename = f"{safe_name}.txt"
                with open(os.path.join(self.output_base, filename), "w", encoding="utf-8") as f:
                    f.write(final_text)

                # Find next internal links
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(self.base_url, link['href'])
                    if self.domain in full_url:
                        self.scrape_site(full_url)

        except Exception as e:
            print(f"Failed to scrape {current_url}: {e}")


if __name__ == "__main__":
    # Update this to your target site
    target_site = "https://www.hashtechy.com/"
    bot = VectorReadyScraper(target_site)
    bot.scrape_site(target_site)
    print("\n✅ Scraping complete. Check the 'formatted_texts' folder.")
