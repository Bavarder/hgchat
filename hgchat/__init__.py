import json 
import requests
import random
import string
from requests_toolbelt import MultipartEncoder
__version__ = "0.1.1"

class Chat:
    def __init__(self, id:int) -> None:
        self.id = id

    @property
    def url(self):
        return f"https://huggingface.co/chat/conversation/{self.id}"

    
class HGChat:
    url_base = "https://huggingface.co"
    def __init__(self, model:str=None) -> None:
        self.chat = None
        self.session = self.make_session()
        self.model = "OpenAssistant/oasst-sft-6-llama-30b-xor" if model is None else model
        self.accepted_welcome_modal = False

    def make_session(self) -> requests.Session:
        session = requests.Session()
        session.get(url=f"{self.url_base}/chat/")
        return session

    def get_chat(self, id:int=None) -> Chat:
        if self.chat is None:
            self.chat = self.new_chat()
        return self.chat

    def new_chat(self) -> Chat:
        if not self.accepted_welcome_modal:
            boundary = "----WebKitFormBoundary" + ''.join(random.sample(string.ascii_letters + string.digits, 16))
            headers = {
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "Origin": self.url_base,
                "Referer": self.url_base + "/chat/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64",
                "Accept": "application/json",
            }
            welcome_modal_fields = {
                "ethicsModalAccepted": "true",
                "shareConversationsWithModelAuthors": "true",
                "ethicsModalAcceptedAt": "",
                "activeModel": self.model,
            }
            m = MultipartEncoder(fields=welcome_modal_fields, boundary=boundary)
            res = self.session.post(self.url_base + "/chat/settings", headers=headers, data=m)
            self.accepted_welcome_modal = True


        r = self.session.post(url="https://huggingface.co/chat/conversation", json={"model": self.model}, headers={"Content-Type": "application/json"})
        if r.status_code != 200:
            raise Exception(f"Failed to create new conversation: {r.json}")
        else:
            return Chat(id=json.loads(r.text)['conversationId'])
       

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
            data = chunk.decode("utf-8")
            if chunk:
                data = json.loads(chunk[5:])
                if "error" not in data:
                    yield data
                else:
                    print("error: ", data["error"])
                    break

if __name__ == "__main__":
    chat = HGChat()
    for data in chat.ask("Hello"):
        print(data)