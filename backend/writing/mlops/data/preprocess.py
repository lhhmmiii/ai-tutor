import re
import os

class TextPreprocessor:
    def __init__(self, text: str):
        self.text = text

    def delete_nonsense_text(self) -> None:
        match = re.search(r'### Language level', self.text)
        if match:
            self.text = self.text[:match.start()]

    def delete_lines_with_test(self) -> None:
        lines = self.text.splitlines()
        filtered_lines = [line for line in lines if 'test' not in line.lower()]
        self.text = '\n'.join(filtered_lines)

    def remove_extra_whitespace(self) -> None:
        """
        Remove extra whitespace from the text, including leading, trailing, and multiple spaces.
        """
        self.text = re.sub(r'\s+', ' ', self.text).strip()

    def lowercase_text(self) -> None:
        """
        Convert all characters in the text to lowercase.
        """
        self.text = self.text.lower()

    def preprocess(self) -> str:
        self.delete_nonsense_text()
        self.delete_lines_with_test()
        self.remove_extra_whitespace()
        self.lowercase_text()
        return self.text

def preprocess_folder(folder_input: str, folder_output: str) -> None:
    for file in os.listdir(folder_input):
        with open(os.path.join(folder_input, file), "r", encoding="utf-8") as f:
            text = f.read()
            preprocessor = TextPreprocessor(text)
            processed_text = preprocessor.preprocess()
            with open(os.path.join(folder_output, file), "w", encoding="utf-8") as f:
                f.write(processed_text)
    print("Preprocessing completed successfully.")

    
if __name__ == "__main__":
    preprocess_folder("writing/data/raw", "writing/data/preprocessed")

