from django.db import models
from django.contrib.auth.models import User

class Email(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_emails", null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_emails", null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} (from {self.sender} to {self.recipient})"

    @property
    def snippet(self):
        return self.body[:50] + ("..." if len(self.body) > 50 else "")