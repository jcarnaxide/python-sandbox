import argparse
from googletrans import Translator

SOURCE_LANGUAGE = 'en'
SUPPORTED_LANGUAGES = [
    'en',
    'es',
    'zh-CN',
    'de',
    'fr',
    'ja',
    'pt',
    'ru',
    'ko',
    'it',
]

# It took some time, but I ultimately found this list
# https://support.google.com/googleplay/android-developer/answer/9844778?hl=en#zippy=%2Cview-list-of-available-languages
GOOGLE_TRANS_TO_PLAY = {
    'en': 'en-US', # English (US)
    'es': 'es-ES', # Spanish (Spain)
    'de': 'de-DE', # German
    'fr': 'fr-FR', # French
    'ja': 'ja-JP', # Japanese
    'pt': 'pt-BR', # Portuguese (Brazilian)
    'ru': 'ru-RU', # Russian
    'ko': 'ko-KR', # Korean
    'it': 'it-IT', # Italian
}

if __name__=="__main__":

    # Setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('english_text')
    args = parser.parse_args()
    english_text = args.english_text

    # Initialize the translator
    translator = Translator()

    # Translate english_text into each language
    with open('data/google_play_translations.txt', 'w', encoding='utf-8') as file:
        for lang in SUPPORTED_LANGUAGES:
            print(f'Translating language code={lang}')
            translation = translator.translate(english_text, dest=lang, src=SOURCE_LANGUAGE)
            print(translation)
            if lang in GOOGLE_TRANS_TO_PLAY:
                print(f"Overriding lang code for compatibility with Google Play, original={lang}, new={GOOGLE_TRANS_TO_PLAY[lang]}")
                lang = GOOGLE_TRANS_TO_PLAY[lang]
            file.write("\n".join([
                f"<{lang}>",
                translation.text,
                f"</{lang}>\n",
            ]))
