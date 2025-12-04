from django.db import models

class report(models.Model):
    name = models.CharField(max_length=300, verbose_name="نام", null=False, blank=False)
    short_reason = models.CharField(max_length=300, verbose_name="علت اصلی", null=False, blank=False)
    email = models.EmailField(verbose_name = "ایمیل", null=False, blank=False)
    message = models.TextField(verbose_name = "پیام", null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "گزارش"

# Create your models here.