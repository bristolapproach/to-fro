from django.db import models


class Ward(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name}"


class HelpType(models.Model):
    name = models.CharField(max_length=50, null=True)
    private_description_template = models.TextField(
        null=True, blank=True, help_text="Private description will be pre-filled with this text when picking this type of help for a Action")
    public_description_template = models.TextField(
        null=True, blank=True, help_text="Public description will be pre-filled with this text when picking this type of help for a Action")

    def __str__(self):
        return f"{self.name}"
