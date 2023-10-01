from django.contrib import admin
from .models import (InspectionReport, Division,
                     Observation)

# Register your models here.

admin.site.register(InspectionReport)
admin.site.register(Division)
admin.site.register(Observation)


