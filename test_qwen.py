import time
import torch

from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor


MODEL_NAME = "Qwen/Qwen2.5-VL-3B-Instruct"

IMAGE_PATH = "bad_yam.jpg"


print("=" * 60)
print("Qwen2.5-VL-3B Visual Defect Test")
print("=" * 60)

print(f"Model: {MODEL_NAME}")


# ---------------------------------------------------------
# Device
# ---------------------------------------------------------

device = "cpu"

print(f"Device: {device}")


# ---------------------------------------------------------
# Load model
# ---------------------------------------------------------

print("Loading Qwen2.5-VL-3B...")

processor = AutoProcessor.from_pretrained(
    MODEL_NAME,
    use_fast=True,
)

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
)

model.eval()

print("Qwen2.5-VL-3B loaded successfully.")


# ---------------------------------------------------------
# Load image
# ---------------------------------------------------------

image = Image.open(IMAGE_PATH).convert("RGB")

print(f"Image: {IMAGE_PATH}")
print(f"Image size: {image.size}")


# ---------------------------------------------------------
# Question
# ---------------------------------------------------------

question = """
Look carefully at this image.



Describe only what you can visually observe.
"""


print("\nQuestion:")
print(question)

print("\nRunning Qwen...")


# ---------------------------------------------------------
# Build conversation
# ---------------------------------------------------------

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": image,
            },
            {
                "type": "text",
                "text": question,
            },
        ],
    }
]


# ---------------------------------------------------------
# Prepare input
# ---------------------------------------------------------

text = processor.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

inputs = processor(
    text=[text],
    images=[image],
    padding=True,
    return_tensors="pt",
)

inputs = inputs.to(device)


# ---------------------------------------------------------
# Generate
# ---------------------------------------------------------

start_time = time.time()

with torch.no_grad():

    generated_ids = model.generate(
        **inputs,
        max_new_tokens=30,
    )

inference_time = time.time() - start_time


# ---------------------------------------------------------
# Remove input tokens
# ---------------------------------------------------------

generated_ids_trimmed = [
    out_ids[len(in_ids):]
    for in_ids, out_ids in zip(
        inputs.input_ids,
        generated_ids,
    )
]


# ---------------------------------------------------------
# Decode
# ---------------------------------------------------------

output_text = processor.batch_decode(
    generated_ids_trimmed,
    skip_special_tokens=True,
    clean_up_tokenization_spaces=False,
)[0]


# ---------------------------------------------------------
# Result
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("QWEN RESULT")
print("=" * 60)

print(output_text)

print("\n" + "=" * 60)
print(f"Inference time: {inference_time:.2f} seconds")
print("=" * 60)