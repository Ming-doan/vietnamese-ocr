from enum import Enum
import json
from pydantic import BaseModel


class MergeType(str, Enum):
    left = "left"
    right = "right"
    union = "union"
    intersection = "intersection"


class _TemplateItem(BaseModel):
    bboxs: list[tuple[float, float]]
    merge_type: MergeType = MergeType.left
    regex: str | None = None


class Template(BaseModel):
    padding: float = 0.0
    template: dict[str, _TemplateItem]
    non_prediction_labels: list[str] = []


def load_template(name: str) -> Template:
    with open(f"templates/{name}.json") as f:
        _template = json.load(f)
    return Template.model_validate(_template)
