import json
from unittest import mock

import pytest
from django.http import JsonResponse
from ninja.testing import TestClient

from core.views import api
from core.views_schemas import WebhookInvoiceParams

ninja_client = TestClient(api)

WEBHOOK_REQUEST_BODY = {
    "event": {
        "id": "4816763241889792",
        "subscription": "invoice",
        "isDelivered": True,
        "created": "2020-03-26T18:00:00.363220+00:00",
        "log": {
            "id": "5096976731340800",
            "created": "2020-03-26T18:00:05.165485+00:00",
            "errors": [],
            "type": "paid",
            "invoice": {
                "taxId": "20.018.183/0001-80",
                "id": "5730174175805440",
                "city": "São Paulo",
                "fee": 0,
                "streetLine2": "CJ 13",
                "district": "Itaim Bibi",
                "streetLine1": "Av. Faria Lima, 1844",
                "due": "2020-06-21T02:59:59.999999+00:00",
                "workspaceId": "5155165527080960",
                "interest": 1.3,
                "status": "paid",
                "tags": ["war supply", "invoice #1234"],
                "zipCode": "01500-000",
                "line": "34191.09008 64410.047308 71444.640008 7 82920000400000",
                "name": "Iron Bank S.A.",
                "created": "2020-03-25T22:22:41.106321+00:00",
                "barCode": "34197829200004000001090064410047307144464000",
                "amount": 400000,
                "stateCode": "SP",
                "descriptions": []
            }
        },
    }
}


def test_webhook():
    req_body = WEBHOOK_REQUEST_BODY

    with mock.patch(
        "core.service.stark_svc.transfer"
    ) as mock_transfer, mock.patch(
        "starkbank.event.parse",
        return_value={}
    ):
        response = ninja_client.post("/hook", json=req_body)

    assert response.status_code == 200
    assert mock_transfer.assert_called_once_with(name="Iron Bank S.A.", paid_value=400000)

