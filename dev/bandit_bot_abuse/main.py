import os
from copy import deepcopy
from pyrogram import Client, filters
from PIL import Image
import easyocr

api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"

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

app = Client("my_account", api_id, api_hash)

text_cache = None

seq_cache: int = 0

first_hook: bool = True

@app.on_message(filters=filters.user('banditpIaybot') & filters.photo)
async def main(client, message) -> None:
    global text_cache, seq_cache, first_hook
    if not first_hook:
        i = 1
        async for history_message in app.get_chat_history('banditpIaybot'):
            if not i:
                if history_message.text[0] != '❌':
                    text_cache = None
                    seq_cache = 0
                break
            else:
                i -= 1
    else:
        text_cache = None
        first_hook = False
        seq_cache = 0
    if not text_cache:
        try:
            await app.download_media(message, file_name='image.jpg')
        except ValueError:
            print(message)

        image = Image.open('downloads/image.jpg')
        cropped_image = image.crop(box=box)
        cropped_image.save('downloads/cropped_image.jpg')

        result = reader.readtext('downloads/cropped_image.jpg')
        text = result[0][1]
        text_cache = text
        os.remove('downloads/image.jpg')
        os.remove('downloads/cropped_image.jpg')
    else:
        text = text_cache
    print(f'text = {text}')
    answer: str = ''
    print(f'seq_cache: {seq_cache}')
    if len(text) == length:
        index: int = seq_cache
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
    if not answer:
        await message.click('пропустить слово')
        first_hook = True
        async for message_to_call_on in app.get_chat_history('banditpIaybot'):
            await main(client, message_to_call_on)
            break
    else:
        await app.send_message('banditpIaybot', answer)


if __name__ == '__main__':
    app.run()
