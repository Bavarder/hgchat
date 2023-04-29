# Hugging Chat Python

## Installation

### As library

``` shell
pip install hgchat
```

### As an interactive prompt

``` shell
git clone https://github.com/Bavarder/hgchat.git
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

