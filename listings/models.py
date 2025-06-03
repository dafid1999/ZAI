from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='listings')
    tags = models.ManyToManyField(Tag, related_name='listings', blank=True)
    image = models.ImageField(upload_to='listings/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='listings/thumbnails/', null=True, blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorites', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status']), models.Index(fields=['created_at'])]

    def save(self, *args, **kwargs):
        old = Listing.objects.filter(pk=self.pk).first() if self.pk else None

        if old:
            if old.image and self.image != old.image and os.path.isfile(old.image.path):
                os.remove(old.image.path)
            if old.thumbnail and os.path.isfile(old.thumbnail.path):
                os.remove(old.thumbnail.path)

        super().save(*args, **kwargs)

        if self.image:
            try:
                img = Image.open(self.image)
                img.thumbnail((200, 200))
                thumb_io = BytesIO()
                img.save(thumb_io, format=img.format)
                img.close()
                base, ext = os.path.splitext(os.path.basename(self.image.name))
                thumb_filename = f"{base}_thumb{ext}"

                self.thumbnail.save(thumb_filename, ContentFile(thumb_io.getvalue()), save=False)
                super().save(update_fields=['thumbnail'])
            except Exception as e:
                print(f"Thumbnail generation failed: {e}")

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        if self.thumbnail and os.path.isfile(self.thumbnail.path):
            os.remove(self.thumbnail.path)
        super().delete(*args, **kwargs)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='APPROVED')

Listing.add_to_class('published', PublishedManager())
