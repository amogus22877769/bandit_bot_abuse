
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
To run the project you need to configure api_id, api_hash, and, of course the length of the words you are getting with the pixel box the words are taking on the screen. And you also need to parse the list of words, if their length is greater then 5 (read below)
#### main.py
```python
<...>
api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"

length: int = n
box: tuple[int, int, int, int] = (341, 184, 415, 214) # thats an example of 4-letter word box
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
работа -> 👮🏻‍♂️ федерал
and the chain will start by itself.



## Optimizations

You can dowload tgcrypto for pyrogram ptimization, but it requires microsoft c++ to be installed.
Also you can use pytesseract, which is apparently faster then easyocr, but you need to install additional software too.


## Demo





