import sys
sys.path.append(".")

from hgchat import HGChat
hgchat = HGChat()

while True:
    user_input = str(input("> "))
    if user_input == "exit" or user_input == "quit":
        break
    elif user_input == "new":
        hgchat = HGChat()
        print("New conversation started")
        continue
    elif user_input == "help":
        print("Commands: exit | quit, new, help, clear, clearall, about")
        continue
    elif user_input == "":
        continue
    elif user_input == "clear":
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        continue
    elif user_input == "clearall":
        sys.stdout.write("\033[2J")
        sys.stdout.write("\033[H")
        continue
    elif user_input == "about":
        print("HGChat - A CLI for huggingface.co/chat")
        continue
    else:
        chat = hgchat.ask(user_input)
        for i in chat:
            char = i["token"]["text"]
            if char == "</s>":
                sys.stdout.write("\n")
            else:
                sys.stdout.write(char)
            sys.stdout.flush()