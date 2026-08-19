import reflex as rx

from intelliscan.services.api import analyze_image
import asyncio


class VisionState(rx.State):

    # ============================================================
    # IMAGE
    # ============================================================

    # Real filesystem path used by FastAPI
    image_path: str = ""

    # Filename only.
    # The frontend will turn this into the upload URL.
    image_filename: str = ""

    # ============================================================
    # ANALYSIS STATUS
    # ============================================================

    analyzing: bool = False
    status: str = "Ready"

    # ============================================================
    # GEMMA 4 RESULT
    # ============================================================

    crop: str = ""
    external: str = ""
    internal: str = ""
    condition: str = ""
    defect: str = ""

    # ============================================================
    # MODEL INFORMATION
    # ============================================================

    inference_time: float = 0.0
    device: str = ""
    model: str = ""
    task: str = ""

    # ============================================================
    # IMAGE INFORMATION
    # ============================================================

    image_width: int = 0
    image_height: int = 0

    # ============================================================
    # ERROR
    # ============================================================

    error_message: str = ""

    # ============================================================
    # UPLOAD
    # ============================================================

    @rx.event
    async def handle_upload(
        self,
        files: list[rx.UploadFile],
    ):
        """Handle uploaded image."""

        if not files:
            return

        file = files[0]

        try:
            # ----------------------------------------------------
            # Read uploaded file
            # ----------------------------------------------------

            upload_data = await file.read()

            # ----------------------------------------------------
            # Reflex upload directory
            # ----------------------------------------------------

            upload_dir = rx.get_upload_dir()

            upload_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            # ----------------------------------------------------
            # Filename
            # ----------------------------------------------------

            filename = file.name

            # ----------------------------------------------------
            # Save file
            # ----------------------------------------------------

            file_path = upload_dir / filename

            with file_path.open("wb") as output:
                output.write(upload_data)

            # ----------------------------------------------------
            # Store backend filesystem path
            # ----------------------------------------------------

            self.image_path = str(file_path)

            # ----------------------------------------------------
            # Store ONLY filename in state
            #
            # IMPORTANT:
            # Do NOT do:
            #
            # self.image_url = rx.get_upload_url(filename)
            #
            # because get_upload_url() is a frontend Var in this
            # context.
            # ----------------------------------------------------

            self.image_filename = filename

            # ----------------------------------------------------
            # Status
            # ----------------------------------------------------

            self.status = "Image ready for analysis"
            self.error_message = ""

            # ----------------------------------------------------
            # Reset previous analysis
            # ----------------------------------------------------

            self.crop = ""
            self.external = ""
            self.internal = ""
            self.condition = ""
            self.defect = ""

            # ----------------------------------------------------
            # Reset model information
            # ----------------------------------------------------

            self.inference_time = 0.0
            self.device = ""
            self.model = ""
            self.task = ""

            # ----------------------------------------------------
            # Reset image dimensions
            # ----------------------------------------------------

            self.image_width = 0
            self.image_height = 0

        except Exception as exc:

            self.error_message = str(exc)
            self.status = "Upload failed"

    

    # ============================================================
    # ANALYZE
    # ============================================================

    @rx.event(background=True)
    async def analyze(self):
        """Send image to FastAPI/Gemma backend."""

        async with self:
            if not self.image_path:
                self.error_message = "Please upload an image first."
                return

            self.analyzing = True
            self.status = "Analyzing image..."
            self.error_message = ""

            image_path = self.image_path

        try:
            response = await asyncio.to_thread(
                analyze_image,
                image_path,
            )

            async with self:
                self.crop = response.get("crop", "")
                self.external = response.get("external", "")
                self.internal = response.get("internal", "")
                self.condition = response.get("condition", "")
                self.defect = response.get("defect", "")

                self.inference_time = response.get(
                    "inference_time",
                    0.0,
                )

                self.device = response.get(
                    "device",
                    "",
                )

                self.model = response.get(
                    "model",
                    "",
                )

                self.task = response.get(
                    "task",
                    "",
                )

                self.image_width = response.get(
                    "image_width",
                    0,
                )

                self.image_height = response.get(
                    "image_height",
                    0,
                )

                self.status = "Analysis complete"

        except Exception as exc:
            async with self:
                self.error_message = str(exc)
                self.status = "Analysis failed"

        finally:
            async with self:
                self.analyzing = False