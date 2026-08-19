import time
import torch

from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM


MODEL_NAME = "microsoft/Florence-2-base"
IMAGE_PATH = "rotten_orange.jpg"

print("=" * 60)
print("Florence-2 Simple VQA Test")
print("=" * 60)

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device: {device}")
print("Loading Florence-2...")

processor = AutoProcessor.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
)

model = model.to(device)
model.eval()

print("Florence-2 loaded successfully.")

image = Image.open(IMAGE_PATH).convert("RGB")

print(f"Image: {IMAGE_PATH}")
print(f"Image size: {image.size}")


# ---------------------------------------------------------
# SIMPLE VQA TEST
# ---------------------------------------------------------

task_prompt = "<VQA>"

question = "What fruit is in the image?"

print("\nQuestion:")
print(question)

print("\nRunning VQA...")

start_time = time.time()

inputs = processor(
    text=task_prompt,
    images=image,
    return_tensors="pt",
)

inputs = {
    key: value.to(device)
    if hasattr(value, "to")
    else value
    for key, value in inputs.items()
}


with torch.no_grad():
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=50,
        num_beams=3,
    )

inference_time = time.time() - start_time

# ---------------------------------------------------------
# Decode generated tokens
# ---------------------------------------------------------

generated_text = processor.batch_decode(
    generated_ids,
    skip_special_tokens=False,
)[0]

print("\nRaw generated text:")
print(repr(generated_text))


# ---------------------------------------------------------
# Florence-2 post processing
# ---------------------------------------------------------

answer = processor.post_process_generation(
    generated_text,
    task=task_prompt,
    image_size=image.size,
)


print("\n" + "=" * 60)
print("FLORENCE-2 RESULT")
print("=" * 60)

print(answer)

print("\n" + "=" * 60)
print(f"Inference time: {inference_time:.2f} seconds")
print("=" * 60)