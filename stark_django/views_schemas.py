from typing import Optional

from ninja import Schema
from pydantic.class_validators import validator


class WebhookInvoiceParams(Schema):
    tag: Optional[str] = None
    integracao: Optional[str] = None
    company_id: Optional[int] = None
    modelo_venda: Optional[str] = None
    grupo_id: Optional[int] = None
    trechoclasse_ids: Optional[str] = None

    @validator("trechoclasse_ids")
    def validate_trechoclasse_ids(cls, v):
        return v.split(",")
