
# BANDIT BOT ABUSE

Stack up your racks (wich you gamble on) in telegeam client of Bandit BOT

## NOTE

Use the dev directory, because src code is unstable and slow, it is prototype and can be used only for understanding project structure

## Installation

Install the additional libraries with pip

```bash
  pip install -r requirements.txt
```
    
## Run locally
To run the project you need to configure api_id, api_hash, and, of course the length of the words you are getting (also you can change the time_to_sleep_to_avoid_flood_wait, read ERROR HANDLING). And you also need to parse the list of words, if their length is greater then 5 (read below)
#### main.py
```python
<...>
api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"

length: int = n
<...>
```
To parse additional n-length words
#### get_words.py
```python
<...>
length = n
<...>
```
```bash
  python main.py
```
Then, you need to go
работа -> 👮🏻‍♂️ федерал or just send random symbol if you are already in the 👮🏻‍♂️ федерал page
and the chain will start by itself.



## Optimizations

You can dowload tgcrypto for pyrogram optimization, but it requires microsoft c++ to be installed.
Also you can use pytesseract, which is apparently faster then easyocr, but you need to install additional software too.


## Error handling
There is a chance that after some usage there will be an error pyrogram.errors.exceptions.flood_420.FloodWait, which is basycally Telegram is telling us our requests/posts are too fast.
Unfortunatly, now I dont know how to fix this issue properly, the dirty solution is just add some sleep to the code. To do that, just change the time_to_sleep_to_avoid_flood_wait variable in main.py. If you have any suggestions, feel free to open a pull request.


## Demo




https://github.com/user-attachments/assets/69beecf3-657b-4bca-abe0-2b1a2a3ab36b


