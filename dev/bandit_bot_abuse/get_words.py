import requests
from bs4 import BeautifulSoup

letters = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "э", "ю", "я"]
words: str = ''
length: int = 5
for letter in letters:
    n = 0
    while True:
        res = requests.get(f'https://поиск-слов.рф/suschestvitelnye/{length}/{letter}?page={n}')
        soup = BeautifulSoup(res.text, 'html.parser')
        wrapped_words = soup.find('div', class_=f"word-length-{length} page-suschestvitelnye")
        if wrapped_words.text[len(wrapped_words.text) - length:] == words[len(words) - length - 1:len(words) - 1]:
            break
        print(wrapped_words.text[len(wrapped_words.text) - length:], words[len(words) - length - 1:len(words) - 1])
        for index, s in enumerate(wrapped_words.text):
            words += s
            if index <= len(wrapped_words.text) - 2:
                if wrapped_words.text[index + 1].isupper():
                    words += '\n'
        words += '\n'
        n += 1

with open(f'{length}_letter_words.txt', 'w', encoding='utf-8') as f:
    f.write(words)
f.close()


