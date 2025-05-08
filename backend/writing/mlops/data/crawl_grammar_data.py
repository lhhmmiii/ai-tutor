import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://learnenglish.britishcouncil.org/grammar/"

names = ["a1-a2-grammar", "b1-b2-grammar", "c1-grammar"]

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


def extract_with_hierarchy(elements, level=0):
    """
    Recursively extracts text content from HTML elements while maintaining hierarchy.

    Args:
        elements (list): A list of Selenium WebElements to process.
        level (int, optional): The current indentation level. Defaults to 0.

    Returns:
        str: A formatted string representation of the extracted content, preserving hierarchy.

    The function processes various HTML tags differently:
    - Headers (h1-h6): Prefixed with '#' based on their level.
    - Paragraphs (p): Included as plain text.
    - Lists (ul, ol): Each item is prefixed with a dash.
    - Other elements: Processed recursively if they have children, otherwise included as plain text.

    Indentation is used to represent the hierarchy of nested elements.
    """
    indent = '  ' * level
    result = ''
    for el in elements:
        tag = el.tag_name.lower()
        text = el.text.strip()

        if not text:
            continue

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            header_level = int(tag[1])
            result += f"{indent}{'#' * header_level} {text}\n"
        elif tag == 'p':
            result += f"{indent}{text}\n"
        elif tag in ['ul', 'ol']:
            items = el.find_elements(By.XPATH, './li')
            for li in items:
                result += f"{indent}- {li.text.strip()}\n"
        else:
            children = el.find_elements(By.XPATH, './*')
            if children:
                result += extract_with_hierarchy(children, level + 1)
            else:
                result += f"{indent}{text}\n"
    return result

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
        
        # Get the main content
        content = driver.find_element(By.CLASS_NAME, 'content')
        elements = content.find_elements(By.XPATH, './*')
        text = extract_with_hierarchy(elements)
        return {'title': title, 'content': text}
        
    except Exception as e:
        print(f"Error parsing lesson at {url}: {str(e)}")
        return None

def crawl_all(save_dir : str = 'writing/data'):
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

if __name__ == "__main__":
    crawl_all()