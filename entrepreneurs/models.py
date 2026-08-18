
import uuid

from django.db import models


class Entrepreneur(models.Model):
    name = models.CharField(max_length=255)

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField()

    profile_image = models.ImageField(
        upload_to="entrepreneurs/profile/",
    )

    video = models.URLField(
        blank=True,
        null=True,
    )

    # =========================================================
    # SOCIAL MEDIA
    # =========================================================

    whatsapp = models.CharField(
        max_length=30,
        blank=True,
    )

    instagram = models.URLField(
        blank=True,
    )

    facebook = models.URLField(
        blank=True,
    )

    tiktok = models.URLField(
        blank=True,
    )

    youtube = models.URLField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    # =========================================================
    # FEATURED
    # =========================================================

    featured = models.BooleanField(
        default=False,
    )

    # =========================================================
    # CREATED DATE
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


class WorkImage(models.Model):
    entrepreneur = models.ForeignKey(
        Entrepreneur,
        related_name="works",
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to="entrepreneurs/works/",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.entrepreneur.name} - Work"


class EntrepreneurLike(models.Model):
    """
    Stores one unique like from a visitor for an entrepreneur.

    A visitor is identified using a UUID stored by the frontend.
    This allows visitors to like profiles without creating an account.
    """

    entrepreneur = models.ForeignKey(
        Entrepreneur,
        related_name="likes",
        on_delete=models.CASCADE,
    )

    visitor_id = models.UUIDField(
        default=uuid.uuid4,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "entrepreneur",
                    "visitor_id",
                ],
                name="unique_entrepreneur_visitor_like",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "entrepreneur",
                    "visitor_id",
                ],
                name="entrepreneur_visitor_idx",
            ),
        ]

        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.visitor_id} liked "
            f"{self.entrepreneur.name}"
        )
