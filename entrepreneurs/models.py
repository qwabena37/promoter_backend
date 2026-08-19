import uuid

from django.db import models


class Entrepreneur(models.Model):

    # =========================================================
    # BASIC INFORMATION
    # =========================================================

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


    # =========================================================
    # PROFILE IMAGE
    # =========================================================

    profile_image = models.ImageField(
        upload_to="entrepreneurs/profile/",
    )


    # =========================================================
    # FEATURED VIDEO
    #
    # Can store:
    # - YouTube URL
    # - TikTok URL
    # - Direct video URL
    # - Cloudinary video URL
    #
    # The frontend decides how to display/play it.
    # =========================================================

    video = models.URLField(
        blank=True,
        null=True,
    )


    # =========================================================
    # SOCIAL MEDIA / CONTACT
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

    linkedIn = models.URLField(
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


    # =========================================================
    # STRING REPRESENTATION
    # =========================================================

    def __str__(self):
        return self.name


# =============================================================
# WORK IMAGE
# =============================================================

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


    # =========================================================
    # MAXIMUM 3 WORK IMAGES
    #
    # When a 4th image is uploaded:
    #
    # 1. Find the oldest image
    # 2. Delete its physical file
    # 3. Delete its database record
    # 4. Save the new image
    #
    # Therefore Cloudinary/storage will not retain
    # the replaced image.
    # =========================================================

    def save(self, *args, **kwargs):

        # Only run this when creating a NEW image
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

            # -------------------------------------------------
            # Maximum of 3 images
            # -------------------------------------------------

            if existing_images.count() >= 3:

                oldest_image = (
                    existing_images.first()
                )

                if oldest_image:

                    # -------------------------------------------------
                    # Delete the actual stored image
                    #
                    # This is important for Cloudinary as well.
                    # -------------------------------------------------

                    if oldest_image.image:

                        oldest_image.image.delete(
                            save=False
                        )

                    # -------------------------------------------------
                    # Delete database record
                    # -------------------------------------------------

                    oldest_image.delete()


        # -----------------------------------------------------
        # Save the new image
        # -----------------------------------------------------

        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return (
            f"{self.entrepreneur.name} - Work"
        )


# =============================================================
# ENTREPRENEUR LIKE
# =============================================================

class EntrepreneurLike(models.Model):

    """
    Stores one unique like from a visitor
    for an entrepreneur.

    A visitor is identified using a UUID
    stored by the frontend.
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


    # =========================================================
    # DATABASE CONSTRAINTS
    # =========================================================

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


    def __str__(self):

        return (
            f"{self.visitor_id} liked "
            f"{self.entrepreneur.name}"
        )