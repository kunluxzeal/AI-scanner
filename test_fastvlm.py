import time
import torch

from PIL import Image
from transformers import AutoProcessor, FastVlmForConditionalGeneration

# ============================================================
# CONFIGURATION
# ============================================================
MODEL_NAME = "KamilaMila/FastVLM-0.5B"
IMAGE_PATH = "rotten_orange.jpg"

print("=" * 60)
print("FastVLM-0.5B Visual Test")
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

# Recommended for generation
processor.tokenizer.padding_side = "left"

print("Processor loaded successfully.")

# ============================================================
# LOAD MODEL
# ============================================================

print("Loading FastVLM-0.5B...")

model = FastVlmForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
)

model = model.to(device)

model.eval()

print("FastVLM-0.5B loaded successfully.")

# ============================================================
# LOAD IMAGE
# ============================================================

image = Image.open(
    IMAGE_PATH
).convert("RGB")

print(f"Image: {IMAGE_PATH}")
print(f"Image size: {image.size}")

# ============================================================
# QUESTION
# ============================================================
question = """
Classify the food crop in this image.

You MUST choose exactly one of these three classes:

Orange
Yam
Sweet Potato

Do not choose any other class.

Ignore defects, damage, color variations, and background.
Identify the crop based only on its overall visual appearance.

Return ONLY one word:
Orange
Yam
Sweet Potato
"""

print("\nQuestion:")
print(question)

print("\nRunning FastVLM...")

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

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
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
        max_new_tokens=50,
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
print("FASTVLM RESULT")
print("=" * 60)

print(output_text)

print("\n" + "=" * 60)
print(
    f"Inference time: {inference_time:.2f} seconds"
)
print("=" * 60)