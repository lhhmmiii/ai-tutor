import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://learnenglish.britishcouncil.org/grammar/"

names = ["a1-a2-grammar", "b1-b2-grammar", "c1-grammar", "english-grammar-reference"]

def init_driver():
    """
    Initialize a Chrome browser using Selenium.
    Returns:
        Selenium WebDriver object
    """
    options = Options()
    # options.add_argument('--headless')  # Optional: Uncomment if you want headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=options)

from selenium.webdriver.common.by import By  # Import By for locating elements

def get_lesson_links(driver, name, max_attempts=50):
    """
    Get all grammar lesson URLs from the main grammar page using Selenium.

    Args:
        driver: Selenium WebDriver
        name: The name of the grammar section (e.g. "a1-a2-grammar")

    Returns:
        List[str]: A list of full URLs for individual grammar lessons
    """
    START_URL = f"{BASE_URL}/{name}"
    driver.get(START_URL)
    time.sleep(3)  # Wait for page to fully load

    # For loop to get all the lesson links
    links = []
    for i in range(1, max_attempts + 1):
            # Generate the current XPath by substituting the number into the base_xpath
            base_xpath = f'//*[@id="block-views-block-taxonomy-term-blocks-block-1"]/div/div/div[1]/div[{i}]/div/div/div[2]/div[1]'
            current_xpath = base_xpath.format(i)
            try:
                # Try to find the element using the dynamically generated XPath
                element = driver.find_element(By.XPATH, current_xpath)
                # Extract the text or attribute from the element (you can modify this part)
                link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if link:
                    links.append(link)
                    print(f"Found link {i}: {link}")
                else:
                    print(f"No link found for element {i}")
            except Exception as e:
                print(f"Element {i} not found. Stopping.")
                break  # Exit the loop if the element is not found

    return links


def parse_lesson(driver, url):
    pass

def crawl_all():
   pass

if __name__ == "__main__":
    links = get_lesson_links(init_driver(), names[1])
    print(links)
