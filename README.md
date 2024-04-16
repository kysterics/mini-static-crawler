Mini Static Crawler
===========================================
### A basic but versatile crawler built to save static webpages in HTML.

<video src="https://github.com/kysterics/mini-static-crawler/assets/63026996/a44079d6-fb18-4900-9bf0-7bae22bbc94d"></video>

<details>
  <summary name="result-demo">:monocle_face: Result (French Wiktionary dictionary) demo</summary>
  
  <video src="https://github.com/kysterics/mini-static-crawler/assets/63026996/0900768b-d629-48b8-a3de-3121beff2843"></video>
  > <picture>
  >   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/tip.svg">
  >   <img alt="Tip" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/tip.svg">
  > </picture><br>
  >
  > Unmute for sound!

</details><br>

Features
-----------------------------
* auto-retry
* recursive search
* progress preservation
* multiprocessing
* progress monitoring
* logging for request attempts
* error handling
* configurable css filter
* http2 support

Configuration
-----------------------------
The configurable options availale along with their default values are listed below:

```python
# scraper config
process_count = 12
cookies = {}
headers = {}

# scraping range
recursive = False
base = ('', )  # base url(s), only required if recursive = True
seed = {f'https://fr.wiktionary.org/?curid={i}' for i in range(1111111)}
entry_css = {'.ns-0', '.ns-14', '.ns-100', '.ns-102', '.ns-104', '.ns-106', '.ns-110', '.ns-114', '.ns-118'}  # css elements to keep
```
<br>

Usage notes
-----------------------------
* Python >=3.10 is recommended.
* To install requirements, use:
  ```properties
  pip install -r requirements.txt
* To start crawling, run:
  ```properties
  python msc.py
* The script is intended to be used on Linux only.
* The script is set up to scrape fr.wiktionary.org for demonstration purposes.
* Variables including those under `# scraper config` and `# scraping range` need to be modified accordingly for different websites.
