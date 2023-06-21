from django_cron import CronJobBase, Schedule

from core.service import stark_svc


class InvoiceIssuer(CronJobBase):
    RUN_EVERY = 180  # Executes every 3h
    TOTAL_BATCHES = 8  # Run for 24h
    batch = 0

    schedule = Schedule(
        run_every_mins=RUN_EVERY,
        retry_after_failure_mins=5
    )
    code = "core.cron.IssueInvoices"  # Identifier

    def do(self):
        if self.batch >= self.TOTAL_BATCHES:
            return

        success = stark_svc.issue_invoices()

        if not success:
            return

        self.batch += 1
