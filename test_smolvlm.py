import time
import torch

from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "HuggingFaceTB/SmolVLM-256M-Instruct"

IMAGE_PATH = "rotten_orange.jpg"


print("=" * 60)
print("SmolVLM-256M Visual Test")
print("=" * 60)

print(f"Model: {MODEL_NAME}")


# ============================================================
# DEVICE
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device: {device}")


# ============================================================
# LOAD PROCESSOR
# ============================================================

print("Loading processor...")

processor = AutoProcessor.from_pretrained(
    MODEL_NAME
)

print("Processor loaded successfully.")


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading SmolVLM-256M...")

model = AutoModelForImageTextToText.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
)

model = model.to(device)

model.eval()

print("SmolVLM-256M loaded successfully.")


# ============================================================
# LOAD IMAGE
# ============================================================

image = Image.open(
    IMAGE_PATH
).convert("RGB")

print(f"Image: {IMAGE_PATH}")
print(f"Image size: {image.size}")


# ============================================================
# SIMPLE QUESTION
# ============================================================

question = """
What fruit or food crop is shown in this image?

Describe only what you can visually observe.
"""


print("\nQuestion:")
print(question)

print("\nRunning SmolVLM...")


# ============================================================
# CONVERSATION
# ============================================================

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
            },
            {
                "type": "text",
                "text": question,
            },
        ],
    }
]


# ============================================================
# PROCESS INPUT
# ============================================================

prompt = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
)


inputs = processor(
    text=prompt,
    images=[image],
    return_tensors="pt",
)


inputs = {
    key: value.to(device)
    for key, value in inputs.items()
    if hasattr(value, "to")
}


# ============================================================
# GENERATION
# ============================================================

start_time = time.time()


with torch.no_grad():

    generated_ids = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=False,
    )


inference_time = time.time() - start_time


# ============================================================
# DECODE
# ============================================================

output_text = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)[0]


# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 60)
print("SMOLVLM RESULT")
print("=" * 60)

print(output_text)

print("\n" + "=" * 60)
print(
    f"Inference time: {inference_time:.2f} seconds"
)
print("=" * 60)






