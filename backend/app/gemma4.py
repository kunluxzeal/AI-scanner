import io
import os
import time
from typing import Any

from PIL import Image

import litert_lm
from litert_lm import Backend
from litert_lm import Content
from litert_lm import Contents
from litert_lm import SamplerConfig
from litert_lm import ThinkingConfig


class Gemma4Service:
    def __init__(self):
        self.model_name = "Gemma 4 E2B"

        self.model_path = os.getenv(
            "GEMMA4_MODEL_PATH",
            os.path.expanduser(
                "~/.litert-lm/cache/huggingface/"
                "litert-community/gemma-4-E2B-it-litert-lm/"
                "gemma-4-E2B-it.litertlm"
            ),
        )

        self.cpu_threads = int(
            os.getenv("GEMMA4_CPU_THREADS", "4")
        )

        print(f"[INFO] Loading {self.model_name}...")
        print(f"[INFO] Model: {self.model_path}")
        print(f"[INFO] CPU threads: {self.cpu_threads}")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Gemma 4 model not found: {self.model_path}"
            )

        # ---------------------------------------------------------
        # LOAD MODEL ONCE
        # ---------------------------------------------------------

        self.engine = litert_lm.Engine(
            self.model_path,
            backend=Backend.CPU(
                thread_count=self.cpu_threads
            ),
            vision_backend=Backend.CPU(
                thread_count=self.cpu_threads
            ),
            max_num_tokens=1024,
            max_num_images=1,
        )

        print("[INFO] Gemma 4 loaded successfully.")

    # -------------------------------------------------------------
    # CREATE A FRESH CONVERSATION FOR EVERY REQUEST
    # -------------------------------------------------------------

    def _create_conversation(self):
        return self.engine.create_conversation(
            sampler_config=SamplerConfig(
                top_k=1,
                top_p=1.0,
                temperature=0.0,
            ),
            thinking_config=ThinkingConfig(
                enable_thinking=False,
                thinking_token_budget=0,
            ),
            max_output_tokens=128,
        )

    # -------------------------------------------------------------
    # IMAGE -> JPEG BYTES
    # -------------------------------------------------------------

    def _image_to_bytes(
        self,
        image: Image.Image,
    ) -> bytes:

        if image.mode != "RGB":
            image = image.convert("RGB")

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=95,
        )

        return buffer.getvalue()

    # -------------------------------------------------------------
    # CROP INSPECTION
    # -------------------------------------------------------------

    def inspect_crop(
        self,
        image: Image.Image,
    ) -> dict[str, Any]:

        start_time = time.perf_counter()

        # Convert image
        image_bytes = self._image_to_bytes(image)

        # ---------------------------------------------------------
        # STRICT INSPECTION PROMPT
        # ---------------------------------------------------------

        prompt = """
You are a STRICT food-crop quality inspector.

Examine the ENTIRE image carefully before making a decision.

Identify the crop:
Yam, Sweet Potato, or Orange.

Then inspect every visible part of the crop for ABNORMALITY.

IMPORTANT:
Do NOT classify a clearly abnormal region as normal simply because
the rest of the crop looks healthy.

Look specifically for localized regions that are visually different
from the surrounding healthy tissue.

EXTERNAL SURFACE:

Look for:

- fuzzy or hairy growth
- grey patches
- green patches
- white patches
- black patches
- brown patches
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
- abnormal texture

A localized region that is clearly different in colour, texture,
shape, or appearance from the surrounding healthy surface MUST be
reported as an abnormality.

Do NOT dismiss a clearly localized abnormal region as
"natural colour variation".

Pay particular attention to:

- isolated dark regions
- black regions
- grey regions
- brown regions
- green regions
- fuzzy regions
- sunken regions
- visibly degraded regions

If one clearly abnormal region is visible, the crop is DEFECTIVE.

INTERNAL TISSUE:

If the crop is cut, sliced, peeled, or broken and flesh is visible,
inspect the exposed flesh separately.

Look for:

- black tissue
- dark brown tissue
- brown discoloration
- abnormal colour
- rot
- mold
- decay
- damaged tissue
- cavities
- unusual texture
- degraded tissue

If internal tissue cannot be seen, write:

Internal: NOT VISIBLE

IMPORTANT DECISION RULE:

GOOD =
No clearly visible abnormal region exists.

DEFECTIVE =
At least ONE clearly visible abnormal region exists on either:

1. the external surface
OR
2. exposed internal tissue.

Do NOT require the entire crop to look damaged.

A single clearly visible defect is sufficient for DEFECTIVE.

Use ONLY visible evidence.

Do not infer hidden damage.

Return ONLY these five lines:

Crop: <Yam|Sweet Potato|Orange>
External: <NONE|short visible description>
Internal: <NONE|NOT VISIBLE|short visible description>
Condition: <GOOD|DEFECTIVE>
Defect: <NONE|short visible description>
""".strip()

        contents = Contents.of(
            Content.ImageBytes(image_bytes),
            Content.Text(prompt),
        )

        # ---------------------------------------------------------
        # IMPORTANT:
        # CREATE A NEW CONVERSATION FOR EVERY IMAGE
        # ---------------------------------------------------------

        conversation = self._create_conversation()

        try:

            response = conversation.send_message(
                contents,
                max_output_tokens=128,
                thinking_config=ThinkingConfig(
                    enable_thinking=False,
                    thinking_token_budget=0,
                ),
            )

        finally:

            # Do not retain the conversation between requests.
            conversation = None

        elapsed_time = (
            time.perf_counter() - start_time
        )

        text = self._extract_text(response)

        parsed = self._parse_response(text)

        return {
            "task": "crop_inspection",
            "model": self.model_name,
            "device": "cpu",
            "inference_time": round(
                elapsed_time,
                3,
            ),
            "image_width": image.width,
            "image_height": image.height,
            "crop": parsed["crop"],
            "external": parsed["external"],
            "internal": parsed["internal"],
            "condition": parsed["condition"],
            "defect": parsed["defect"],
            "raw_response": text,
        }

    # -------------------------------------------------------------
    # COMPATIBILITY METHOD
    # -------------------------------------------------------------

    def object_detection(
        self,
        image: Image.Image,
    ) -> dict[str, Any]:

        return self.inspect_crop(image)

    # -------------------------------------------------------------
    # EXTRACT MODEL TEXT
    # -------------------------------------------------------------

    @staticmethod
    def _extract_text(
        response: Any,
    ) -> str:

        if isinstance(response, dict):

            content = response.get(
                "content",
                [],
            )

            if isinstance(content, list):

                parts = []

                for item in content:

                    if isinstance(item, dict):

                        text = item.get("text")

                        if text:
                            parts.append(text)

                if parts:
                    return "\n".join(parts).strip()

            if isinstance(content, str):
                return content.strip()

        return str(response).strip()

    # -------------------------------------------------------------
    # PARSE RESPONSE
    # -------------------------------------------------------------

    @staticmethod
    def _parse_response(
        text: str,
    ) -> dict[str, str]:

        result = {
            "crop": "Unknown",
            "external": "NONE",
            "internal": "NOT VISIBLE",
            "condition": "GOOD",
            "defect": "NONE",
        }

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for line in lines:

            if ":" not in line:
                continue

            key, value = line.split(
                ":",
                1,
            )

            key = key.strip().upper()
            value = value.strip()

            if key == "CROP":
                result["crop"] = value

            elif key == "EXTERNAL":
                result["external"] = value

            elif key == "INTERNAL":
                result["internal"] = value

            elif key == "CONDITION":
                result["condition"] = value

            elif key == "DEFECT":
                result["defect"] = value

        # ---------------------------------------------------------
        # NORMALIZE CONDITION
        # ---------------------------------------------------------

        condition = result["condition"].upper()

        if "DEFECTIVE" in condition:
            result["condition"] = "DEFECTIVE"

        elif "GOOD" in condition:
            result["condition"] = "GOOD"

        # ---------------------------------------------------------
        # NORMALIZE CROP
        # ---------------------------------------------------------

        crop = result["crop"].strip()

        if crop.lower() == "yam":
            result["crop"] = "Yam"

        elif crop.lower() in ["sweet potato", "sweetpotato"]:
            result["crop"] = "Sweet Potato"

        elif crop.lower() == "orange":
            result["crop"] = "Orange"

        return result

    # -------------------------------------------------------------
    # CLOSE MODEL
    # -------------------------------------------------------------

    def close(self):

        if hasattr(self, "engine") and self.engine is not None:

            self.engine.close()

            self.engine = None

        print("[INFO] Gemma 4 resources released.")


# -------------------------------------------------------------
# SINGLE GLOBAL MODEL INSTANCE
# -------------------------------------------------------------

gemma4_service = Gemma4Service()