from django.db import models


class Entrepreneur(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    bio = models.TextField()

    profile_image = models.ImageField(
        upload_to="entrepreneurs/profile/"
    )

    video = models.FileField(
        upload_to="entrepreneurs/videos/",
        blank=True,
        null=True
    )

    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkImage(models.Model):
    entrepreneur = models.ForeignKey(
        Entrepreneur,
        related_name="works",
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="entrepreneurs/works/"
    )