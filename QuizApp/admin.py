from django.contrib import admin
from .models import *

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Participant)
admin.site.register(QuizResult)