from django.db import models
import random


class PaymentModel(models.Model):
    locale = models.CharField(max_length=10, default='tr')
    conversationId = models.CharField(max_length=10, blank=True)
    token = models.CharField(max_length=50, default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            _id: str = ''
            for _ in range(10):
                _id += f'{random.randint(0, 9)}'
            self.conversationId = _id
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.locale} - {self.conversationId}'
