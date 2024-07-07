from django.contrib import admin
from polls.models import Question,Answer,Vote

# Register your models here.
admin.site.register(
[    Question,
    Answer,
    Vote]
)