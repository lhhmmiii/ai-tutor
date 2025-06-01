import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def load_vocabulary_data(file_path: str):
    df = pd.read_excel(file_path, usecols=['Word', 'Definitons'])
    words = df['Word'].tolist()
    definitions = df['Definitons'].tolist()
    return words, definitions



def crawl_wiktionary(word):
    url = f"https://en.wiktionary.org/wiki/{word}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    ipa = soup.find("span", class_="IPA")

    return {
        'word': word,
        'ipa': ipa.text if ipa else 'N/A',
    }




def fetch_wiktionary_data(words, definitions, output_dir):
    
    os.makedirs(output_dir, exist_ok=True)
    for i, word in enumerate(words):
        res = crawl_wiktionary(word)
        text = f"Word: {word}\nDefinitions: {definitions[i]}\nIPA: {res['ipa']}"
        
        # Create a valid filename from the word
        filename = "".join(x for x in word if x.isalnum() or x in [' ', '-', '_']).rstrip()
        filename = filename.replace(' ', '_') + '.txt'
        
        # Save the data to a text file
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Data for word '{word}' saved to {filename}")

if __name__ == "__main__":
    words, definitions = load_vocabulary_data('app/data/vocabulary/NGSL_1.2_with_English_definitions.xlsx')
    fetch_wiktionary_data(words, definitions, 'app/data/vocabulary/wiktionary_data')


