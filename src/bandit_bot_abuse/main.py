import asyncio
import os
from copy import deepcopy
from time import sleep

from pyrogram import Client
from PIL import Image
import easyocr
import pytesseract
import builtins

original_open = open
def bin_open(filename, mode='rb'):       # note, the default mode now opens in binary
    return original_open(filename, mode)


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
print(pytesseract.get_languages())

length: int = 4
box: tuple[int, int, int, int] = (341, 184, 415, 214)

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
        return [
            [seq[0], seq[1]],
            [seq[1], seq[0]]
        ]
    else:
        res: list[list[list[int]]] = []
        for index, el in enumerate(seq):
            c = deepcopy(seq)
            c.pop(index)
            res.append(list_multiplication(el, get_sequences(c)))
        return [
            seq
            for wrapped_seq in res
            for seq in wrapped_seq
        ]

seqs: list[list[int]] = get_sequences(list(range(length)))

cache = None
#api_id = 12345
#api_hash = "0123456789abcdef0123456789abcdef"

api_id = 21273837
api_hash = 'bc317131b0accad2d5bfe360d0593c60'

async def get_image(num: int) -> None:
    async with Client("my_account", api_id, api_hash) as app:
        async for message in app.get_chat_history('banditpIaybot'):
            await message.download(file_name='image.jpg')
            break

async def is_working(num: int) -> bool:
    async with Client("my_account", api_id, api_hash) as app:
        while True:
            if await app.get_chat_history_count('banditpIaybot') >= num:
                break
            sleep(0.1)
        i: int = 1
        async for message in app.get_chat_history('banditpIaybot'):
            print(message.text)
            if not i:
                return False if message.text[0] == '❌' else True
            else:
                i -= 1

async def send_answer(ans: str) -> None:
    async with Client("my_account", api_id, api_hash) as app:
        await app.send_message('banditpIaybot', ans)

async def get_number_of_messages() -> int:
    async with Client("my_account", api_id, api_hash) as app:
        return await app.get_chat_history_count('banditpIaybot')

def send_solve(number_of_messages, depth=0):
    global cache
    if not cache:
        asyncio.run(get_image(number_of_messages))

        image = Image.open('downloads/image.jpg')
        cropped_image = image.crop(box=box)
        cropped_image.save('downloads/cropped_image.jpg')

        result = reader.readtext('downloads/cropped_image.jpg')
        text = result[0][1]
        #builtins.open = bin_open
        #text = pytesseract.image_to_string('downloads/image.jpg', lang='rus')
        #builtins.open = original_open
        print(f'text = {text}')
        cache = text
        os.remove('downloads/image.jpg')
        os.remove('downloads/cropped_image.jpg')
    else:
        text = cache
    answer: str = ''
    print(f'depth: {depth}')
    for seq in seqs:
        guess: str = ''
        for el in seq:
            guess += text[el]
        print(f'guess = {guess}')
        if guess in words and not depth:
            answer = guess
            break
        elif guess in words:
            depth -= 1
    print(f'answer = {answer}')
    asyncio.run(send_answer(answer))
def main():
    number_of_messages = asyncio.run(get_number_of_messages())
    while True:
        send_solve(number_of_messages)
        number_of_messages += 3
        depth = 1
        while not asyncio.run(is_working(number_of_messages)):
            print('not_working')
            send_solve(number_of_messages, depth=depth)
            depth += 1
            number_of_messages += 3
        global cache
        cache = None


if __name__ == '__main__':
    main()
