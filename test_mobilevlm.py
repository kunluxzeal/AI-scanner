import sys
import time
import torch
from PIL import Image
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
from huggingface_hub import hf_hub_download
import os

MODEL_NAME = "mtgv/MobileVLM_V2-1.7B"
IMAGE_PATH = "rotten_orange.jpg"

# Download custom modeling files
model_dir = hf_hub_download(MODEL_NAME, filename="modeling_mobilevlm.py", repo_type="model")
model_dir = model_dir.rsplit('/', 1)[0]
sys.path.insert(0, model_dir)

print("=" * 60)
print("MobileVLM V2 1.7B Visual Test")
print("=" * 60)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
print("Tokenizer loaded.")

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    device_map=device
)
model.eval()
print("Model loaded.")

image = Image.open(IMAGE_PATH).convert("RGB")
print(f"Image: {IMAGE_PATH}")

question = """
Inspect this food crop image.
The crop must be exactly ONE of: Orange, Yam, Sweet Potato
First identify the crop.
Then inspect ONLY the visible surface for: mold, rot, dark spots, black spots, brown spots, discoloration, bruising, cuts, cracks, abnormal areas
Do not infer hidden damage.
Do not invent defects.
Return exactly:
Crop: [Orange / Yam / Sweet Potato]
Condition: [GOOD / DEFECTIVE]
Defects: [NONE / visible defects only]
Use only visible evidence.
"""

prompt = f"USER: <image>\n{question}\nASSISTANT:"
inputs = tokenizer(prompt, return_tensors="pt")
inputs = {key: value.to(device) for key, value in inputs.items() if hasattr(value, "to")}

print("\nRunning inference...")
start_time = time.time()

with torch.no_grad():
    output_ids = model.generate(**inputs, max_new_tokens=40, do_sample=False)

inference_time = time.time() - start_time

output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("\n" + "=" * 60)
print("RESULT")
print("=" * 60)
print(output_text)
print(f"\nInference time: {inference_time:.2f} seconds")

cd ~/llama.cpp && time ./build/bin/llama-mtmd-cli \
  -hf 'ZiangWu/MobileVLM_V2-1.7B-GGUF' \
  --chat-template vicuna \
  --image ~/Documents/intelliscan/bad_yam.jpg \
  -t 4 -tb 4 -n 120 --temp 0.0 \
  -p "You are an expert agricultural botanist in West Africa specializing in tuber identification.

Distinguish between these two tubers using these explicit visual rules:
- TRUE YAM (Dioscorea): Rough, dark brown, bark-like skin with visible fibrous hair/whiskers, rough cut ends, cylindrical or cylindrical-blocky shape.
- SWEET POTATO: Smooth, reddish-brown, purple, or light orange thin skin, tapered/pointed ends, oblong shape, no rough bark texture.
- ORANGE: Round citrus fruit with pitted orange or green peel.

Step 1: Look closely at the skin texture and shape. Is it rough/bark-like/cylindrical (Yam) or smooth/tapered (Sweet Potato)?
Step 2: Inspect for rot, mold, soft decay spots, deep cuts, or sprouting.

Output strictly in this format:
SKIN_TEXTURE: [Rough bark-like OR Smooth thin skin]
CROP: [Yam | Orange | Sweet Potato]
STATUS: [GOOD | DEFECTIVE]"