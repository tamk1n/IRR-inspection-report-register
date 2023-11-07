from celery import shared_task
from datetime import date

@shared_task
def set_ir_status(ir_id):

    from irr_app.models import InspectionReport

    ir = InspectionReport.objects.filter(id=ir_id).first()

    if ir is None:
        raise ValueError(f"InspectionReport with ID {ir_id} not found")
    
    ir.status = 'Overdue'
    
    ir.save()
    return ir.status
