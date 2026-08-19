import uuid

from django.db import models


# =========================================================
# ENTREPRENEUR
# =========================================================

class Entrepreneur(models.Model):

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    name = models.CharField(
        max_length=255,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField()

    # =====================================================
    # PROFILE IMAGE
    # =====================================================

    profile_image = models.ImageField(
        upload_to="entrepreneurs/profile/",
    )

    # =====================================================
    # FEATURED VIDEO
    # =====================================================

    video = models.URLField(
        blank=True,
        null=True,
    )

    # =====================================================
    # SOCIAL MEDIA / CONTACT
    # =====================================================

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

    linkedIn = models.URLField(
        blank=True,
    )

    # =====================================================
    # FEATURED
    # =====================================================

    featured = models.BooleanField(
        default=False,
    )

    # =====================================================
    # CREATED DATE
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):
        return self.name


# =========================================================
# WORK IMAGE
# =========================================================

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

    # =====================================================
    # MAXIMUM 3 WORK IMAGES
    # =====================================================

    def save(self, *args, **kwargs):

        # Only enforce the limit when creating
        # a completely new image.
        if not self.pk:

            existing_images = (
                WorkImage.objects
                .filter(
                    entrepreneur=self.entrepreneur
                )
                .order_by(
                    "created_at",
                    "id",
                )
            )

            if existing_images.count() >= 3:

                oldest_image = (
                    existing_images.first()
                )

                if oldest_image:

                    # Delete physical file
                    if oldest_image.image:

                        oldest_image.image.delete(
                            save=False
                        )

                    # Delete database record
                    oldest_image.delete()

        super().save(
            *args,
            **kwargs
        )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (
            f"{self.entrepreneur.name} - Work"
        )


# =========================================================
# ENTREPRENEUR LIKE
# =========================================================

class EntrepreneurLike(models.Model):

    """
    Stores one unique like from a visitor.

    Each visitor is identified by a UUID stored
    in the frontend localStorage.

    One visitor can only have one like per
    entrepreneur.
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

    # =====================================================
    # DATABASE SETTINGS
    # =====================================================

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "entrepreneur",
                    "visitor_id",
                ],
                name=(
                    "unique_entrepreneur_visitor_like"
                ),
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

        ordering = [
            "-created_at",
        ]

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (
            f"{self.visitor_id} liked "
            f"{self.entrepreneur.name}"
        )