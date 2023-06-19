# import json
# import logging
# from datetime import datetime
from django.http import JsonResponse
from ninja import NinjaAPI

import service.stark_svc as stark_svc
from views_schemas import WebhookInvoiceParams
from stark_auth import project
import starkbank

api = NinjaAPI()
starkbank.user = project

@api.post("/hook")
def invoice_webhook(request):
    event = starkbank.event.parse(
        signature = request.headers["Digital-Signature"],
        content = request.data.decode("utf-8")
    )

    print(event.log.invoice)

    # body = WebhookInvoiceParams.parse_raw(request.body)
    # stark_svc.tranfer(body)

    return JsonResponse({"success": True})
