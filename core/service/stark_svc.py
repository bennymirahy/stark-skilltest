from datetime import date, datetime
from random import randint

import names
import logging
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


def send_invoices():
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

    starkbank.user = project
    starkbank.invoice.create(invoices)

    logger.info(f"{datetime.today().isoformat()}: {quant_invoices} invoices were issued")


def transfer(a, b, c):
    pass
