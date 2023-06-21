import logging
from datetime import date, datetime
from random import randint

import names
import starkbank
from cpf_generator import CPF

from .stark_auth import project

# Logging config
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def issue_invoices():
    # Creates random invoices
    quant_invoices = randint(8, 12)
    invoices = []
    for _ in range(quant_invoices):
        invoices.append(
            starkbank.Invoice(
                amount=randint(20, 1000),
                tax_id=CPF.format(CPF.generate()),
                name=names.get_full_name(),
                due=date.today().isoformat()
            )
        )

    # Attempts to issue the invoices
    starkbank.user = project  # Sets sandbox auth credencials
    try:
        starkbank.invoice.create(invoices)
    except Exception as ex:
        logger.exception(f"{datetime.today().isoformat()}: Something went wrong while issuing the invoices")
        return False

    logger.info(f"{datetime.today().isoformat()}: {quant_invoices} invoices were issued")
    return True


def transfer(paid_value):
    transfer_specs = {
        "amount": int(paid_value),
        "tax_id": "20.018.183/0001-80",
        "name": "Stark Bank S.A.",
        "bank_code": "20018183",
        "branch_code": "0001",
        "account_number": "6341320293482496",
        "account_type": "payment",
        "rules": [
            starkbank.transfer.Rule(
                key="resendingLimit", value=3
            )
        ]
    }
    starkbank_transfer = starkbank.Transfer(**transfer_specs)

    try:
        starkbank.transfer.create([starkbank_transfer])
    except Exception as ex:
        logger.exception(f"{datetime.today().isoformat()}: Something went wrong while transfering {paid_value}")
        return False

    logger.info(f"{datetime.today().isoformat()}: {paid_value} was transfered to Stark Bank S.A.'s account")
    return True

