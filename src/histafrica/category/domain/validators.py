from typing import Dict
from rest_framework import serializers
from histafrica.shared.domain.validators import (
    DRFValidator,
    StrictBooleanField,
    StrictCharField,
)
import logging


class CategoryRules(serializers.Serializer):
    name = StrictCharField(max_length=255)
    description = StrictCharField(required=False, allow_null=True, allow_blank=True)
    is_active = StrictBooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)


class CategoryValidator(DRFValidator):
    def validate(self, data: Dict) -> bool:
        logger = logging.getLogger(__name__)
        logger.info(f"Validating: {data}")  # is not display when run pytest
        rules = CategoryRules(data=data if data is not None else {})
        return super().validate(rules)


class CategoryValidatorFactory:

    @staticmethod
    def create():
        return CategoryValidator()
