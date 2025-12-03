from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Software(models.Model):
    title = models.CharField(max_length=200, verbose_name="نام نرم‌افزار")
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300, verbose_name="توضیح کوتاه")
    cover_image = models.ImageField(upload_to='software_covers/', verbose_name="تصویر کاور")

    developer = models.CharField(max_length=100, verbose_name="سازنده") # Microsoft
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='softwares', verbose_name="دسته‌بندی")
    
    download_count = models.PositiveIntegerField(default=0, verbose_name="تعداد دانلود")
    
    description = models.TextField(verbose_name="توضیحات کامل") # تب توضیحات کامل
    installation_guide = models.TextField(blank=True, verbose_name="راهنمای نصب") # تب راهنمای نصب
    
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="تگ‌ها")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "نرم‌افزار"
        verbose_name_plural = "نرم‌افزارها"

    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        return 4.9

class Feature(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='features')
    text = models.CharField(max_length=255, verbose_name="ویژگی")

    def __str__(self):
        return self.text


class SoftwareRelease(models.Model):
    PLATFORM_CHOICES = (
        ('win', 'Windows'),
        ('mac', 'macOS'),
        ('linux', 'Linux'),
        ('android', 'Android'),
    )

    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='releases')
    version = models.CharField(max_length=50, verbose_name="نسخه") # v2024.1
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, verbose_name="پلتفرم")
    
    specific_install_guide = models.TextField(blank=True, verbose_name="راهنمای نصب اختصاصی این نسخه")
    
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "نسخه/ریلیز"
        verbose_name_plural = "نسخه‌ها"
        unique_together = ('software', 'version', 'platform')

    def __str__(self):
        return f"{self.software.title} - {self.version} ({self.platform})"

class FilePart(models.Model):
    release = models.ForeignKey(SoftwareRelease, on_delete=models.CASCADE, related_name='parts')
    part_number = models.PositiveSmallIntegerField(default=1, verbose_name="شماره پارت")
    download_link = models.URLField(max_length=500, verbose_name="لینک دانلود")
    file_size = models.CharField(max_length=50, verbose_name="حجم", help_text="مثال: 2 GB")
    
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "پارت دانلود"
        verbose_name_plural = "پارت‌های دانلود"
        ordering = ['part_number']

    def __str__(self):
        return f"{self.release} - Part {self.part_number}"