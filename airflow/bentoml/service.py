from __future__ import annotations
from bentoml.validators import ContentType
from typing import Annotated
from PIL.Image import Image
from pydantic import Field
import bentoml
from pathlib import Path

LOCAL_WEIGHTS_PATH = "best.pt"

@bentoml.service(name="YoloV8")
class YoloV8:
    # bento_model = bentoml.keras.get("celestial_bodies_classifier_model")
    def __init__(self) -> None:
        from ultralytics import YOLO
        # self.preprocess = self.bento_model.custom_objects["preprocess"]
        # self.postprocess = self.bento_model.custom_objects["postprocess"]
        # self.model = self.bento_model.load_model()

        self.model = YOLO(LOCAL_WEIGHTS_PATH)

    @bentoml.api()
    def predict(
        self,
        image: Annotated[Image, ContentType("image/jpeg")] = Field(description="Image to analyze"),
    ) -> Annotated[str, ContentType("application/json")]:
        # image = self.preprocess(image)
        prediction = self.model.predict(image)[0]

        # return json.dumps(self.postprocess(predictions))
        return prediction.tojson()
    
    @bentoml.api
    def render(
        self, 
        image: Annotated[Path, ContentType("image/*")] = Field(description="Image to analyze")
    ) -> Annotated[Path, ContentType("image/*")]:
        prediction = self.model.predict(image)[0]
        output = image.parent.joinpath(f"{image.stem}_result{image.suffix}")
        prediction.save(str(output))
        return output