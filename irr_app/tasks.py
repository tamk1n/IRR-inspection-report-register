from celery import shared_task
from datetime import datetime
import pytz

@shared_task
def set_ir_status(ir_id):

    # importing here to prevent circular import error
    from irr_app.models import InspectionReport

    ir = InspectionReport.objects.filter(id=ir_id).first()
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    if (ir.close_date and ir.target_date < ir.close_date) or (now > ir.target_date):
        ir.status = 'Overdue'
    elif ir.closed:
        ir.status = 'Close'
    else:
        ir.status = 'Open'