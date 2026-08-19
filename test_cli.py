cd ~/Documents/intelliscan

time uv run litert-lm run \
  --from-huggingface-repo litert-community/gemma-4-E2B-it-litert-lm \
  gemma-4-E2B-it.litertlm \
  --attachment ~/Documents/intelliscan/good_orange_multi.jpg \
  --vision-backend cpu \
  --cpu-thread-count 4 \
  --temperature 0.0 \
  --thinking false \
  --max-num-tokens 1024 \
  --prompt "You are a STRICT food-crop quality inspector.

Examine the ENTIRE image carefully before making a decision.

Identify the crop:
Yam, Sweet Potato, or Orange.

Then inspect every visible part of the crop for ABNORMALITY.

IMPORTANT:
Do NOT classify a clearly abnormal region as normal simply because the rest of the crop looks healthy.

Look specifically for localized regions that are visually different from the surrounding healthy tissue.

EXTERNAL SURFACE:
Look for:
- fuzzy or hairy growth
- grey, green, white, black, or brown patches
- mold-like growth
- dark spots
- black spots
- brown spots
- rotting areas
- bruises
- sunken areas
- damaged skin
- unusual discoloration
- cracks
- holes
- cuts
- decay

A localized grey, green, white, black, or brown patch that appears substantially different from the surrounding healthy surface MUST be reported as an abnormality when clearly visible.

Do NOT dismiss such a region as 'natural colour variation' unless it genuinely appears consistent with the normal appearance of the crop.

INTERNAL TISSUE:
If the crop is cut, sliced, peeled, or broken and flesh is visible, inspect the exposed flesh separately.

Look for:
- black or dark brown tissue
- abnormal discoloration
- rot
- mold
- decay
- damaged tissue
- cavities
- unusual texture

If internal tissue cannot be seen, write:
Internal: NOT VISIBLE

DECISION:

GOOD = no clearly visible abnormal region.

DEFECTIVE = at least ONE clearly visible abnormal region exists on the external surface OR exposed internal tissue.

Use ONLY visible evidence.
Do not infer hidden damage.

Return ONLY:

Crop: <Yam|Sweet Potato|Orange>
External: <NONE|short description>
Internal: <NONE|NOT VISIBLE|short description>
Condition: <GOOD|DEFECTIVE>
Defect: <NONE|short description>"