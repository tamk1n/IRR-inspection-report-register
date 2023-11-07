sudo docker-compose run irr_web python manage.py startapp {app_name}
sudo docker-compose run irr_web python manage.py makemigrations

flower:
        build: .
        container_name: flower
        command: celery -A irr.celery flower --port=5555
        ports:
            - 5555:5555
        volumes: 
            - ./usr/src/app
        depends_on:
            - irr_web
            - redis
            - celery


            
"""from irr_app.models import InspectionReport

    ir = InspectionReport.objects.filter(id=ir_id).first()

    if ir is None:
        raise ValueError(f"InspectionReport with ID {ir_id} not found")
    
    if ir.close_date:
        ir.status = 'Close'
    ir.save()"""

    if ir is None:
        raise ValueError(f"InspectionReport with ID {ir_id} not found")