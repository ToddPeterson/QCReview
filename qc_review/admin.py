from django.contrib import admin

from .models import QCRun, SuiteRun

admin.site.register(QCRun)
admin.site.register(SuiteRun)
