import time

import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor


class FlorenceService:
    def __init__(self):
        self.device = (
            "cuda:0"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.torch_dtype = (
            torch.float16
            if torch.cuda.is_available()
            else torch.float32
        )

        self.model_name = "microsoft/Florence-2-base"

        print(
            f"[INFO] Loading Florence-2 on {self.device}..."
        )

        self.model = (
            AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=self.torch_dtype,
                trust_remote_code=True,
            )
            .to(self.device)
        )

        self.processor = (
            AutoProcessor.from_pretrained(
                self.model_name,
                trust_remote_code=True,
            )
        )

        self.model.eval()

        print("[INFO] Florence-2 loaded successfully.")

    def object_detection(
        self,
        image: Image.Image,
    ) -> dict:

        start_time = time.perf_counter()

        task_prompt = "<OD>"

        inputs = self.processor(
            text=task_prompt,
            images=image,
            return_tensors="pt",
        ).to(
            self.device,
            self.torch_dtype,
        )

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
            do_sample=False,
        )

        generated_text = (
            self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=False,
            )[0]
        )

        parsed_answer = (
            self.processor.post_process_generation(
                generated_text,
                task=task_prompt,
                image_size=(
                    image.width,
                    image.height,
                ),
            )
        )

        elapsed_time = (
            time.perf_counter() - start_time
        )

        result = parsed_answer["<OD>"]

        return {
            "task": "object_detection",
            "model": self.model_name,
            "device": self.device,
            "inference_time": round(
                elapsed_time,
                3,
            ),
            "image_width": image.width,
            "image_height": image.height,
            "detections": result,
        }


florence_service = FlorenceService()