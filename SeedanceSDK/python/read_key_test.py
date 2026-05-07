# 测试使用.env文件读取密钥
import os
from dotenv import load_dotenv
# 1. 加载 .env 文件
load_dotenv()
def read_key():
    api_key:str = os.environ.get("ARK_API_KEY")
    # 2. 加上 f，否则打印不出来变量值
    # print(f"你的 API Key 是: {api_key}")
    return api_key

# 3. 必须手动调用 main 函数，否则程序只是加载了定义就退出了
if __name__ == "__main__":
    read_key()