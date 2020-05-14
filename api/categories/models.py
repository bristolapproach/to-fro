from django.db import models


class Ward(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name}"


class HelpType(models.Model):
    name = models.CharField(max_length=50, null=True)
    icon_name = models.CharField(
        max_length=50, null=True, help_text="Name of the fontawesome icon used to represent this type of help (among the 'free' ones: https://fontawesome.com/icons?d=gallery&m=free)")
    private_description_template = models.TextField(
        null=True, blank=True, help_text="Private description will be pre-filled with this text when picking this type of help for a Action")
    public_description_template = models.TextField(
        null=True, blank=True, help_text="Public description will be pre-filled with this text when picking this type of help for a Action")

    def __str__(self):
        return f"{self.name}"


class Requirement(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"
