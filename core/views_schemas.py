from decimal import Decimal as D
from typing import Optional

from django.core.exceptions import ValidationError
from ninja import Schema
from pydantic import StrictFloat
from pydantic.class_validators import validator


class WebhookInvoiceParams(Schema):
    name: Optional[str] = None
    amount: StrictFloat
    fee: StrictFloat

    @validator("amount")
    def positive_currency(v):
        if v <= 0:
            raise ValidationError

    def currency_to_decimal(cls):
        base_dict = cls.dict()
        amount = base_dict.pop("amount")
        fee = base_dict.pop("fee")
        base_dict["paid_value"] = D(amount) - D(fee)
        return base_dict
