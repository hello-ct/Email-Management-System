from django.contrib import admin
from .models import Email

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "recipient", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("subject", "body", "sender__username", "recipient__username")
    ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.subject} (from {self.sender} to {self.recipient})"

    @property
    def snippet(self):
        return self.body[:50] + ("..." if len(self.body) > 50 else "")