from intelliscan.services.api import analyze_image


result = analyze_image("good_yam.jpg")

print(result)




cd ~/llama.cpp

./build/bin/llama-mtmd-cli \
  -hf 'ggml-org/Qwen2.5-VL-3B-Instruct-GGUF:Q4_K_M' \
  --image ~/Documents/intelliscan/rotten_orange.jpg \
  --image-min-tokens 256 \
  -t 4 \
  -tb 4 \
  -n 50 \
  -p "Analyze this food crop image carefully.

Identify the food crop shown in the image. It may be yam, sweet potato, orange, potato, or another crop.

Return exactly four lines:

Crop: [actual crop name]
Condition: [GOOD or DEFECTIVE]
Defects: [NONE or visible defects only]
Confidence: [HIGH, MEDIUM, or LOW]

Important:
- Do not assume the crop is yam, sweet potato, orange, or potato.
- If it is another crop, identify that crop instead.
- Do not infer hidden damage or spoilage.
- Report only defects that are visibly present.
- If you cannot reliably identify the crop, write:
  Crop: UNKNOWN
  Confidence: LOW"