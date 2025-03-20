import time
import random
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Undetected ChromeDriver
import undetected_chromedriver as uc

# Selenium exceptions
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

# Optional: webdriver-manager for auto-downloading ChromeDriver
try:
    from webdriver_manager.chrome import ChromeDriverManager
    AUTO_DOWNLOAD = True
except ImportError:
    AUTO_DOWNLOAD = False

# A small pool of user-agents to randomly choose from
USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
    # Chrome on Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    # Firefox on Linux
    "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36 Edg/114.0.0.0",
]

def get_driver():
    """
    Creates an undetected-chromedriver instance with random user-agent,
    random window size, and increased timeouts.
    """
    user_agent = random.choice(USER_AGENTS)

    options = uc.ChromeOptions()

    # If you want it visually, comment out the headless
    # options.add_argument("--headless=new")

    # Random window size
    width = random.randint(1000, 1600)
    height = random.randint(700, 900)
    options.add_argument(f"--window-size={width},{height}")

    # Set the random user agent
    options.add_argument(f"--user-agent={user_agent}")

    # Additional arguments to reduce detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    if AUTO_DOWNLOAD:
        driver = uc.Chrome(
            driver_executable_path=ChromeDriverManager().install(),
            options=options,
        )
    else:
        driver = uc.Chrome(options=options)

    # Set page load timeout: the driver will wait up to 180s for a page to load
    driver.set_page_load_timeout(300)

    return driver


def scrape_powerball():
    """
    Attempts to scrape Powerball results from usamega.com/powerball/results/<page>
    - uses advanced Selenium measures (undetected-chromedriver, random user agent).
    - sets a page load timeout and retries on TimeoutException
    - random sleeps between pages
    - stops if older than 5 years, or no more next page link

    Returns:
      List of dictionaries with fields:
        Draw Date, White Balls, Powerball, Jackpot
    """
    base_url = "https://www.usamega.com/powerball/results/"
    page = 1

    # Collect only last 5 years
    five_years_ago = datetime.now() - timedelta(days=5 * 365)

    all_records = []
    driver = get_driver()

    try:
        while True:
            url = f"{base_url}{page}"
            print(f"[INFO] Attempting to load page: {url}")

            # We'll allow up to 3 retries for each page in case of timeouts
            max_retries = 3
            success = False

            for attempt in range(max_retries):
                try:
                    driver.get(url)
                    success = True
                    break  # loaded successfully
                except TimeoutException:
                    print(f"[WARNING] Timeout loading page {url} (attempt {attempt+1}/{max_retries}). Retrying...")
                    time.sleep(3)  # short sleep before retry
                except WebDriverException as e:
                    # If we get a different error, you might want to handle or log it
                    print(f"[ERROR] WebDriverException on page {url}: {e}")
                    success = False
                    break

            if not success:
                print("[ERROR] Could not load page after retries. Stopping.")
                break

            # Random sleep so we don't appear too bot-like
            time.sleep(random.uniform(2, 5))

            # Grab final rendered HTML
            html = driver.page_source

            # Check for Cloudflare block or suspicious content
            if any(
                phrase in html
                for phrase in ["cf-error-details", "Access Denied", "You have been blocked"]
            ):
                print("[WARNING] Cloudflare or site block detected. Stopping.")
                break

            soup = BeautifulSoup(html, "html.parser")

            # find rows
            rows = soup.select("table.results.pb tbody tr")
            if not rows:
                print(f"[INFO] No rows found on page {page}, stopping pagination.")
                break

            found_any = False

            for tr in rows:
                tds = tr.find_all("td")
                if len(tds) < 2:
                    continue

                # FIRST <td> => date, numbers
                date_a = tds[0].select_one("section.results a")
                if not date_a:
                    continue

                date_text = date_a.get_text(strip=True)
                # e.g., "Wed, March, 19, 2025"
                parts = [p.strip() for p in date_text.split(",")]
                if len(parts) < 4:
                    continue

                # parse date
                # parts ~ ["Wed", "March", "19", "2025"]
                date_str_for_parse = f"{parts[1]} {parts[2]} {parts[3]}"
                try:
                    draw_date = datetime.strptime(date_str_for_parse, "%B %d %Y")
                except ValueError:
                    continue

                # If older than 5 years, break from entire scraping
                if draw_date < five_years_ago:
                    print("[INFO] Encountered a draw older than 5 years. Stopping.")
                    return all_records

                draw_date_str = draw_date.strftime("%m/%d/%Y")

                # White balls + Powerball
                ul = tds[0].select_one("section.results ul")
                if not ul:
                    continue

                li_tags = ul.find_all("li")
                white_balls = []
                power_ball = None

                for li in li_tags:
                    classes = li.get("class", [])
                    val = li.get_text(strip=True)
                    if "bonus" in classes:
                        power_ball = val  # red ball
                    elif "multiplier" in classes:
                        pass  # ignoring multiplier
                    else:
                        white_balls.append(val)

                if len(white_balls) < 5 or not power_ball:
                    continue

                # SECOND <td> => jackpot
                jackpot_a = tds[1].find("a")
                jackpot_str = jackpot_a.get_text(strip=True) if jackpot_a else ""

                record = {
                    "Draw Date": draw_date_str,
                    "White Balls": " ".join(white_balls[:5]),
                    "Powerball": power_ball,
                    "Jackpot": jackpot_str,
                }
                all_records.append(record)
                found_any = True

            if not found_any:
                print(f"[INFO] No valid draws found on page {page}, stopping.")
                break

            # Check if there's a next-page link
            next_link = soup.select_one(f'a.button[href="/powerball/results/{page+1}"]')
            if next_link:
                # random sleep before next page
                time.sleep(random.uniform(2, 6))
                page += 1
            else:
                print("[INFO] No next-page link found; finishing.")
                break

    finally:
        driver.quit()

    return all_records


def main():
    records = scrape_powerball()
    df = pd.DataFrame(records, columns=["Draw Date", "White Balls", "Powerball", "Jackpot"])
    df.to_csv("powerball_results_advanced.csv", index=False)
    print(f"[INFO] Total records scraped: {len(df)}. Saved to powerball_results_advanced.csv.")


if __name__ == "__main__":
    main()
