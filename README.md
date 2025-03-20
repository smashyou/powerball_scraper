# Lottery Scraper

This Python script scrapes **Powerball** and **Mega Millions** lottery results from [www.usamega.com](https://www.usamega.com). It extracts the following information:

- **Draw Date**
- **Winning Numbers (White Balls)**
- **Powerball/Mega Ball**
- **Jackpot Amount**

The scraped data is saved to a `.csv` file for further analysis or record-keeping.

---

## Features
- **Advanced Scraping**: Uses Selenium with `undetected-chromedriver` to avoid detection and bypass anti-bot measures.
- **Randomized Behavior**: Randomizes user agents, window sizes, and sleep times to mimic human behavior.
- **Robust Error Handling**: Retries on timeouts and handles Cloudflare blocks gracefully.
- **Date Filtering**: Scrapes only the last 5 years of lottery results.
- **CSV Export**: Saves the scraped data to a `.csv` file.

---

## Requirements
### **Python Version**
- **Python 3.11**: Ensure you have Python 3.11 installed, as all libraries are tested and compatible with this version.

### **Libraries**
Install the required libraries using `pip`:
```bash
pip install pandas beautifulsoup4 selenium undetected-chromedriver webdriver-manager
```

- `pandas`: For organizing and exporting data to a `.csv` file.
- `beautifulsoup4`: For parsing HTML and extracting data.
- `selenium`: For browser automation (used to handle JavaScript-rendered content).
- `undetected-chromedriver`: To avoid detection while using Selenium with Chrome.
- `webdriver-manager`: (Optional) Automatically downloads and manages the ChromeDriver executable.

---

## How to Use
1. **Clone or Download the Script**:
   - Download the script or clone the repository to your local machine.

2. **Install Dependencies**:
   - Run the following command to install the required libraries:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Script**:
   - Execute the script using Python:
     ```bash
     python lottery_scraper.py
     ```

4. **Output**:
   - The script will scrape the data and save it to a `.csv` file named `lottery_winning_numbers.csv`.

---

## Example Output
The script generates a `.csv` file with the following columns:
- **Draw Date**: The date of the lottery draw.
- **White Balls**: The winning white ball numbers.
- **Powerball/Mega Ball**: The winning Powerball or Mega Ball number.
- **Jackpot**: The jackpot amount for the draw.

Example `.csv` output:
```
Draw Date,White Balls,Powerball,Jackpot
03/20/2025,10 20 30 40 50,25,$100 Million
03/17/2025,05 15 25 35 45,10,$200 Million
```

---

## Code Overview
### **Key Functions**
1. **`get_driver()`**:
   - Configures an undetected ChromeDriver instance with a random user agent, window size, and additional options to avoid detection.

2. **`scrape_powerball()`**:
   - Scrapes Powerball results from `usamega.com`.
   - Handles timeouts, retries, and Cloudflare blocks.
   - Filters results to only include draws from the last 5 years.

3. **`main()`**:
   - Calls `scrape_powerball()` to collect data and saves it to a `.csv` file.

---

## Script Details
### **Imports**
The script uses the following libraries:
- `time`: For adding delays between requests.
- `random`: For randomizing user agents and sleep times.
- `pandas`: For organizing and exporting data.
- `datetime`: For filtering results by date.
- `BeautifulSoup`: For parsing HTML content.
- `selenium`: For browser automation.
- `undetected_chromedriver`: To avoid detection while using Selenium.

### **User Agents**
A pool of user agents is used to randomize requests and avoid detection:
```python
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 ...",
    "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
]
```

### **Scraping Logic**
- The script navigates through multiple pages of lottery results.
- It extracts the draw date, winning numbers, and jackpot amount.
- Results older than 5 years are ignored.

### **Error Handling**
- The script retries up to 3 times if a page fails to load.
- It checks for Cloudflare blocks and stops scraping if detected.

---

## Notes
- **Anti-Bot Measures**: The script uses `undetected-chromedriver` and randomizes behavior to avoid detection. However, if the website updates its anti-bot measures, the script may need adjustments.
- **Compliance**: Ensure you comply with the website's `robots.txt` file and terms of service when scraping data.
- **Performance**: The script includes random sleep times to mimic human behavior, which may slow down the scraping process.

---

## License
This project is open-source and available under the MIT License.
```

---

### Key Sections in the `README.md`:
1. **Overview**: Explains the purpose and features of the script.
2. **Requirements**: Lists Python 3.11 and all necessary libraries.
3. **Usage Instructions**: Provides step-by-step instructions for running the script.
4. **Example Output**: Describes the `.csv` file format and example output.
5. **Code Overview**: Summarizes the key functions and their roles.
6. **Script Details**: Explains the imports, user agents, scraping logic, and error handling.
7. **Notes**: Includes important considerations like anti-bot measures and compliance.
