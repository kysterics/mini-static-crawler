Mini Static Crawler
===========================================
### A basic but versatile crawler built to save static webpages in HTML.

<video src="https://github.com/kysterics/mini-static-crawler/blob/main/demo/msc-demo.mp4" alt="msc demo">
<video src="https://github.com/kysterics/mini-static-crawler/blob/main/demo/result-demo.mp4" alt="result demo">
<details>
  <summary>GIF demo</summary>

  ![demo](https://ptpimg.me/l48mm0.gif)
  :warning: Use [this link](https://ptpimg.me/l48mm0.gif) if the GIF fails to render.
</details>
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
