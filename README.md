# Lottery Scraper

This Python script scrapes the winning numbers of lottery games (Powerball or Mega Millions) from the website [www.usamega.com](https://www.usamega.com). It extracts the following information:

- **Winning Numbers**
- **Date of the Drawing**
- **Jackpot Amount**

The scraped data is then exported to a `.csv` file for further analysis or record-keeping.

---

## Features
- Scrapes lottery data for Powerball and Mega Millions.
- Extracts:
  - Winning numbers
  - Date of the drawing
  - Jackpot amount
- Exports the data to a `.csv` file.

---

## Requirements
To run this script, you need the following:

### **Python Version**
- **Python 3.11**: Ensure you have Python 3.11 installed, as all libraries are tested and compatible with this version.

### **Libraries**
Install the required libraries using `pip`:
```bash
pip install requests beautifulsoup4 pandas selenium undetected-chromedriver
