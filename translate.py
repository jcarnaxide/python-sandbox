import argparse
import re
import pandas as pd
from googletrans import Translator

SOURCE_LANGUAGE = 'en'
GODOT_TO_GOOGLE_LANG_CODE_OVERRIDES = {
    'zh': 'zh-CN' # Chinese Simplified
}

def google_placeholder(i: int):
    return f'__PH_{i}__'

# Function to protect placeholders in text
def protect_placeholders(text):
    # Replace placeholders like {0}, {1}, etc., with temporary tokens
    placeholders = re.findall(r'\{[a-zA-Z0-9_]+\}', text)
    print(f'Found {len(placeholders)} placeholders')
    protected_text = text
    for i, placeholder in enumerate(placeholders):
        replacement_text = google_placeholder(i)
        protected_text = protected_text.replace(placeholder, replacement_text)
        print(f'Replacing "{placeholder}" with "{replacement_text}"')
    return protected_text, placeholders

# Function to restore placeholders in translated text
def restore_placeholders(translated_text: str, placeholders):
    print(f'Tranlsated text "{translated_text}"')
    restored_text = translated_text
    for i, placeholder in enumerate(placeholders):
        replaced_text = google_placeholder(i)
        restored_text = restored_text.replace(replaced_text, placeholder)
        print(f'Restoring {replaced_text} as {placeholder}')
    print(f'Restored text "{restored_text}"')
    return restored_text

if __name__=="__main__":

    # Setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_key')
    parser.add_argument('english_text')
    args = parser.parse_args()
    input_key = args.input_key
    english_text = args.english_text

    # Load the CSV file
    df = pd.read_csv('data/text_translation.csv')

    # Initialize the translator
    translator = Translator()

    # Get the list of columns representing languages
    language_columns = df.columns[2:] # Assuming first two columns are key and source text

    # Make any replacements to Godot Lang Codes to match google format
    language_columns = [
        col.replace(godot, google)
        for col in language_columns
        for godot, google in GODOT_TO_GOOGLE_LANG_CODE_OVERRIDES.items()
    ]

    # Update placeholders
    print(english_text)
    protected_text, placeholders = protect_placeholders(english_text)

    # Translate english_text into each language
    translations = {}
    for column in language_columns:
        print(f'Translating language code={column}')

        translation = translator.translate(protected_text, dest=column.lower(), src=SOURCE_LANGUAGE)
        translations[column] = restore_placeholders(translation.text, placeholders)

    # Create a new row with the translations
    translated_row = [input_key, english_text] + [translations[col] for col in language_columns]

    # Add the new translated row to the DataFrame
    df.loc[len(df)] = translated_row

    # Save the updated DataFrame back to a CSV file
    df.to_csv('data/text_translation_updated.csv', index=False)
