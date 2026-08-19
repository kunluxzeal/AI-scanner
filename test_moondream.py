import time
import torch

from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer

# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "vikhyatk/moondream2"
IMAGE_PATH = "rotten_orange.jpg"

print("=" * 60)
print("Moondream Visual Test")
print("=" * 60)

print(f"Model: {MODEL_NAME}")

# ============================================================
# DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device: {device}")

# ============================================================
# LOAD MODEL
# ============================================================

print("Loading Moondream...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
)

model = model.to(device)

print("Moondream loaded successfully.")

# ============================================================
# LOAD IMAGE
# ============================================================

image = Image.open(IMAGE_PATH).convert("RGB")

print(f"Image: {IMAGE_PATH}")
print(f"Image size: {image.size}")

# ============================================================
# QUESTION
# ============================================================

question = """
What fruit or food crop is shown in this image?

Describe only what you can visually observe.
"""

print("\nQuestion:")
print(question)

print("\nRunning Moondream...")

# ============================================================
# ENCODE IMAGE
# ============================================================

start_time = time.time()

image_embeds = model.encode_image(image)

# ============================================================
# ASK QUESTION
# ============================================================

answer = model.answer_question(
    image_embeds,
    question,
    tokenizer,
)

inference_time = time.time() - start_time

# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 60)
print("MOONDREAM RESULT")
print("=" * 60)

print(answer)

print("\n" + "=" * 60)
print(f"Inference time: {inference_time:.2f} seconds")
print("=" * 60)