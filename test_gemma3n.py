import time
import base64
import requests

MODEL = "gemma3n:e2b"
IMAGE_PATH = "/home/jimmy/Documents/intelliscan/bad_yam.jpg"

prompt = """Look at this food crop image carefully.

Identify the crop.

Choose exactly ONE:

Yam
Sweet Potato
Orange

Use only visible evidence.

Answer with ONLY the crop name.
"""

print("=" * 60)
print("Gemma 3n E2B Visual Test")
print("=" * 60)

print(f"Model: {MODEL}")
print(f"Image: {IMAGE_PATH}")

with open(IMAGE_PATH, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

print("\nRunning Gemma 3n...")

start_time = time.time()

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [image_base64],
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 5,
        },
    },
)

total_time = time.time() - start_time

if response.status_code != 200:
    print("\nERROR:")
    print(response.text)
    raise SystemExit(1)

data = response.json()

answer = data["message"]["content"]

print("\n" + "=" * 60)
print("GEMMA 3N RESULT")
print("=" * 60)

print(answer.strip())

print("\n" + "=" * 60)
print(f"Total inference time: {total_time:.2f} seconds")
print("=" * 60)

if "prompt_eval_count" in data:
    print(f"Prompt tokens: {data['prompt_eval_count']}")

if "eval_count" in data:
    print(f"Generated tokens: {data['eval_count']}")

if "eval_duration" in data and data["eval_duration"] > 0:
    tok_per_sec = (
        data["eval_count"] /
        (data["eval_duration"] / 1e9)
    )
    print(f"Generation speed: {tok_per_sec:.2f} tokens/sec")






