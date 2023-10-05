from django.contrib import admin
from .models import Task

# Define la clase TaskAdmin antes de registrar el modelo Task
class TaskAdmin(admin.ModelAdmin):
    list_filter = ('important', 'created', 'dateCompleted')  # Puedes usar campos más adecuados para filtros
    readonly_fields = ("created",)


admin.site.register(Task, TaskAdmin)
