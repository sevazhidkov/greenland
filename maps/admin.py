from django.contrib import admin

from maps import models

admin.site.register(models.LatLngBounds)
admin.site.register(models.MapArea)
admin.site.register(models.Question)
admin.site.register(models.QuestionSet)
admin.site.register(models.AnswerSet)
admin.site.register(models.Answer)
