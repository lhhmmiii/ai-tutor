import os
import sys
import time
import re
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
    options.add_argument('--enable-unsafe-swiftshader')
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
    """
    Parse a single grammar lesson page to extract content.
    
    Args:
        driver: Selenium WebDriver instance
        url: URL of the lesson page to parse
        
    Returns:
        dict: Dictionary containing lesson title, explanation, examples and exercises
    """
    driver.get(url)
    time.sleep(2)  # Wait for page to load
    
    try:
        # Get the lesson title
        title = driver.find_element(By.CLASS_NAME, 'page-header').text
        
        # Get the example
        p1_xpath = '//*[@id="block-block-group-main-content"]/article/div/div[3]/p[1]'
        b1_xpath = '//*[@id="block-block-group-main-content"]/article/div/div[3]/blockquote[1]'

        p1_text = driver.find_element(By.XPATH, p1_xpath).text.strip()
        b1_text = driver.find_element(By.XPATH, b1_xpath).text.strip()
        example_str = p1_text + "\n\n" + b1_text
        # Get the grammar explanation
        grammar_elements = driver.find_element(By.XPATH, '//*[@id="block-block-group-main-content"]/article/div/div[3]/h2')
        siblings = grammar_elements.find_elements(By.XPATH, 'following-sibling::*')
        grammar_explanation_text = []
        allowed_tags = {"p", "h3", "blockquote"}
        text_content = []
        for elem in siblings:
            tag = elem.tag_name
            if tag == "h2":  # Stop when encountering a new major heading
                break
            if tag in allowed_tags:
                text_content.append(elem.text.strip())
        grammar_explanation_text = '\n'.join(text_content)
        return {'title': title, 'content': example_str + '\n\n' + grammar_explanation_text}

    except Exception as e:
        print(f"Error parsing lesson at {url}: {str(e)}")
        return None

def crawl_all(save_dir : str = 'writing/data/grammar/raw'):
    """
    Crawl all grammar lessons from all sections.
    
    This function initializes a web driver, gets lesson links for each grammar section,
    and parses each lesson page to extract content.
    
    Returns:
        None
    """
    driver = init_driver()
    
    try:
        for name in names:
            print(f"Crawling section: {name}")
            lesson_links = get_lesson_links(driver, name)
            
            # Create the save directory if it doesn't exist
            os.makedirs(save_dir, exist_ok=True)
            
            for url in lesson_links:
                lesson_data = parse_lesson(driver, url)
                if lesson_data:
                    title = lesson_data['title']
                    content = lesson_data['content']
                    
                    # Create a valid filename from the title
                    filename = "".join(x for x in title if x.isalnum() or x in [' ', '-', '_']).rstrip()
                    filename = filename.replace(' ', '_') + '.txt'
                    
                    # Save the content to a text file
                    with open(os.path.join(save_dir, filename), 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Saved lesson: {filename}")
                time.sleep(1)  
                
    except Exception as e:
        print(f"Error during crawling: {str(e)}")
    finally:
        driver.quit()


def remove_extra_whitespace(text) -> None:
    """
    Remove extra whitespace from the text, including leading, trailing, and multiple spaces.
    """
    text = re.sub(r'\s+', ' ', text).strip()

def lowercase_text(text) -> None:
    """
    Convert all characters in the text to lowercase.
    """
    text = text.lower()

def preprocess_folder(folder_input: str, folder_output: str) -> None:
    for file in os.listdir(folder_input):
        with open(os.path.join(folder_input, file), "r", encoding="utf-8") as f:
            text = f.read()
            processed_text = lowercase_text(remove_extra_whitespace(text))
            with open(os.path.join(folder_output, file), "w", encoding="utf-8") as f:
                f.write(processed_text)
    print("Preprocessing completed successfully.")

if __name__ == "__main__":
    crawl_all()
    preprocess_folder("app/data/grammar/raw", "app/data/grammar/preprocessed")
