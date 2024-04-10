Mini Static Crawler
===========================================
### A basic but versatile crawler built to save static webpages in HTML.

<video src="https://github.com/kysterics/mini-static-crawler/assets/63026996/4d1c0307-a89e-453e-b40a-9711ab137a45"></video>

<details>
  <summary>Result (French Wiktionary dictionary) demo</summary>
  <video src="https://github.com/kysterics/mini-static-crawler/assets/63026996/0900768b-d629-48b8-a3de-3121beff2843"></video>
</details>

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
