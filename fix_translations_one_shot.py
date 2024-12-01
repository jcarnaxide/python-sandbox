import pandas as pd

if __name__ == "__main__":
    # Load the CSV file
    df = pd.read_csv('data/text_translation_to_fix.csv')
    for language_to_drop in ['ar', 'he']:
        df.drop(language_to_drop, axis=1, inplace=True)
    df.to_csv('data/fixed_translation.csv', encoding='utf-8', index=False)
