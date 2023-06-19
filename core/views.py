# import json
# import logging
# from datetime import datetime
import starkbank
from django.http import JsonResponse
from ninja import NinjaAPI

from .service import stark_svc
from .service.stark_auth import project
from .views_schemas import WebhookInvoiceParams

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
