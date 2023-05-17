# Hugging Chat Python

**Warn**: This repo isn't maintained anymore. Use [Soulter/hugging-chat-api](https://github.com/Soulter/hugging-chat-api) instead.

## Installation

### As library

#### From Pypi

``` shell
pip install hgchat
```

#### From Codeberg

``` shell
pip install --index-url https://codeberg.org/api/packages/Bavarder/pypi/simple/ hgchat
```

### As an interactive prompt

``` shell
git clone https://codeberg.org/Bavarder/hgchat.git # or https://github.com/Bavarder/hgchat.git
cd hgchat
```

## Usage

### As library

``` python
from hgchat import HGChat
hgchat = HGChat()

r = hgchat.ask(user_input)
for i in r:
    char = i["token"]["text"]
    if char == "</s>":
        print("\n", end="")
    else:
        print(char, end="")
```

### As an interactive prompt

``` shell
python chat.py
```

