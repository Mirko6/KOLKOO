from googletrans import Translator

translator = Translator()
translated = translator.translate('', src='sk')
print(translated.text)