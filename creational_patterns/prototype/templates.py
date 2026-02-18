from typing import Dict
from creational_patterns.prototype.config import JobConfig


class JobTemplates:
    _templates: Dict[str, JobConfig] = {}

    @classmethod
    def register(cls, key: str, template: JobConfig) -> None:
        cls._templates[key] = template

    @classmethod
    def get(cls, key: str) -> JobConfig:
        if key not in cls._templates:
            raise ValueError(f"Template with key {key} not found")
        return cls._templates[key].clone()
