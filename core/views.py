# import json
# import logging
# from datetime import datetime
import starkbank
from django.http import JsonResponse
from django.shortcuts import render
from ninja import NinjaAPI

from .service import stark_svc
from .service.stark_auth import project
from .views_schemas import WebhookInvoiceParams

api = NinjaAPI()
starkbank.user = project

@api.post("/hook")
def invoice_webhook(request):
    try:
        event = starkbank.event.parse(
            signature=request.headers["Digital-Signature"],
            content=request.data.decode("utf-8")
        )
    except Exception:
        return JsonResponse({"success": False}, status=400)

    if event.log.type != "paid":
        # Invoice nao pago
        return JsonResponse({"success": True})

    paid_invoice = event.log.invoice
    paid_invoice = WebhookInvoiceParams.parse_obj(paid_invoice).currency_to_decimal()
    stark_svc.transfer(**paid_invoice)

    return JsonResponse({"success": True})


def index(request):
    return render(request, "index.html")
