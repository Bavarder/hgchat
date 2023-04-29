import json 
import requests

class Chat:
    def __init__(self, id:int) -> None:
        self.id = id

    @property
    def url(self):
        return f"https://huggingface.co/chat/conversation/{self.id}"

    
class HGChat:
    def __init__(self) -> None:
        self.chat = None
        self.session = self.make_session()

    def make_session(self) -> requests.Session:
        session = requests.Session()
        session.get(url="https://huggingface.co/chat/")
        return session

    def get_chat(self, id:int=None) -> Chat:
        if self.chat is None:
            self.chat = self.new_chat()
        return self.chat

    def new_chat(self) -> Chat:
        r = self.session.post(url="https://huggingface.co/chat/conversation")
        if r.status_code != 200:
            raise Exception("Failed to create new conversation")
        else:
            return Chat(id=r.json()["conversationId"])
       

    def ask(self, message:str, temperature: float = 0.9, top_p: float = 0.95, repetition_penalty: float = 1.2, top_k: int = 50, truncate: int = 1024, watermark: bool = False, max_new_tokens: int = 1024) -> None:
        self.get_chat()
        r = self.session.post(
            url=self.chat.url, 
            json={
                "inputs": message,
                "parameters": {
                    "temperature": temperature,
                    "top_p": top_p,
                    "repetition_penalty": repetition_penalty,
                    "top_k": top_k,
                    "truncate": truncate,
                    "watermark": watermark,
                    "max_new_tokens": max_new_tokens,
                    "stop": [
                    "<|endoftext|>"
                    ],
                    "return_full_text": False
                },
                "stream": True,
                "options": {
                    "use_cache": False
                }
            },
            stream=True
        )
        if r.status_code != 200:
            raise Exception("Failed to send message")

        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                data = json.loads(chunk.decode("utf-8")[5:])
                if "error" not in data:
                    yield data
                else:
                    print("error: ", data["error"])
                    break
