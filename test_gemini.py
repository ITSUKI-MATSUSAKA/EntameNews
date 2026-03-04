import os
import os
import google.generativeai as genai

# 環境変数からAPIキーを取得
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("エラー: 環境変数 GEMINI_API_KEY が設定されていません。")
    exit(1)

genai.configure(api_key=API_KEY)
models = [m.name for m in genai.list_models()]
with open("models.txt", "w") as f:
    f.write("\n".join(models))
print("Done writing to models.txt")
