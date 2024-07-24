
import requests

res = requests.post(
    "http://127.0.0.1:11434/api/chat",  # 服务器地址
    json={
        "model": "codellama",  # 使用 codellama 模型
        "stream": False,  # 禁用流式输出
        "messages": [
            {"role": "user", "content": "你是谁？"},  # 用户输入
        ],
    },
)
print(res.json())


