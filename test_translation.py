#Tigrinya
from deep_translator import GoogleTranslator

# Use any translator you like, in this example GoogleTranslator
translated = GoogleTranslator(source='auto', target='ti').translate("red")  # output -> Weiter so, du bist großartig
print(translated)