import os
from copy import deepcopy
from time import sleep
from pyrogram import Client, filters
from PIL import Image
import easyocr

api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"
username = 'banditpIaybot'
length: int = 5

time_to_sleep_to_avoid_flood_wait = 3

box: tuple[int, int, int, int] = (341, 184, 400 + (length - 3) * 15, 214)

with open(f'{length}_letter_words.txt', encoding='utf-8', mode='r') as f:
    list_of_words: list[str] = f.read().split()
f.close()

words: set[str] = set(map(lambda x:
                          x.upper().replace('Ё', 'Е'), list_of_words))

reader = easyocr.Reader(['ru'])

def list_multiplication(a: int, b: list[list[int]]) -> list[list[int]]:
    res: list[list[int]]= []
    for seq in b:
        seq.insert(0, a)
        res.append(seq)
    return res

def get_sequences(seq: list[int]) -> list[list[int]]:
    if len(seq) == 2:
        if seq[0] != seq[1]:
            return [
                [seq[0], seq[1]],
                [seq[1], seq[0]]
            ]
        else:
            return [
                [seq[0], seq[0]]
            ]
    else:
        res: list[list[list[int]]] = []
        first_symbols: set[int] = set()
        for index, el in enumerate(seq):
            if el not in first_symbols:
                c = deepcopy(seq)
                c.pop(index)
                res.append(list_multiplication(el, get_sequences(c)))
                first_symbols.add(el)
        return [
            seq
            for wrapped_seq in res
            for seq in wrapped_seq
        ]


seqs = None

app = Client("my_account", api_id, api_hash)

text_cache = None

seq_cache: int = 0

first_hook: bool = True

last_message_caption = None

@app.on_message(filters=filters.user(username) & filters.photo)
async def main(client, message) -> None:
    sleep(time_to_sleep_to_avoid_flood_wait)
    global text_cache, seq_cache, first_hook, seqs, last_message_caption
    if not first_hook:
        if last_message_caption != message.caption:
            text_cache = None
            seq_cache = 0
            seqs = None
            last_message_caption = message.caption
    else:
        text_cache = None
        first_hook = False
        seq_cache = 0
        seqs = None
    if not text_cache:
        await app.download_media(message, file_name='image.jpg')

        image = Image.open('downloads/image.jpg')
        cropped_image = image.crop(box=box)
        cropped_image.save('downloads/cropped_image.jpg')

        result = reader.readtext('downloads/cropped_image.jpg')
        text = result[0][1]
        text_cache = text
        os.remove('downloads/image.jpg')
        os.remove('downloads/cropped_image.jpg')

        seqs = get_sequences([index if letter not in text[:index] else text.index(letter) for index, letter in enumerate(text)])
    else:
        text = text_cache
    print(f'text = {text}')
    answer: str = ''
    print(f'seq_cache: {seq_cache}')
    if len(text) == length:
        for index in range(seq_cache, len(seqs)):
            guess: str = ''
            for el in seqs[index]:
                guess += text[el]
            print(f'guess = {guess}')
            if guess in words:
                answer = guess
                seq_cache = index + 1
                break
    print(f'answer = {answer}')
    if not answer or answer == 'ТЕКСТ':
        await message.click('пропустить слово')
        first_hook = True
        async for message_to_call_on in app.get_chat_history(username):
            await main(client, message_to_call_on)
            break
    else:
        await app.send_message(username, answer)


if __name__ == '__main__':
    app.run()
