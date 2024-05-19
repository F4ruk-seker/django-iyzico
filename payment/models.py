from django.db import models
import random


class PaymentModel(models.Model):
    locale = models.CharField(max_length=10, default='tr')
    conversationId = models.CharField(max_length=10, blank=True)
    token = models.CharField(max_length=50, default=None, blank=True, null=True)

    # status vs.. burada tutulabilir

    @staticmethod
    def generate_random_id(length=10):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    def save(self, *args, **kwargs):
        if not self.pk and not self.conversationId:
            self.conversationId = self.generate_random_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.locale} - {self.conversationId}'
