from django.db import models
from django.utils.translation import gettext_lazy as _


class Ward(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name}"


class Requirement(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"


class HelpType(models.Model):
    name = models.CharField(max_length=50, null=True)
    icon_name = models.CharField(
        max_length=50, blank=True, null=True, help_text="Name of the fontawesome icon used to represent this type of help (among the 'free' ones: https://fontawesome.com/icons?d=gallery&m=free)")
    private_description_template = models.TextField(
        null=True, blank=True, help_text="Private description will be pre-filled with this text when picking this type of help for a Action")
    public_description_template = models.TextField(
        null=True, blank=True, help_text="Public description will be pre-filled with this text when picking this type of help for a Action")
    requirements = models.ManyToManyField(Requirement, blank=True, related_name="help_types",
                                          verbose_name="Default requirements",
                                          help_text="New actions with this help type will get these requirements by default. The requirements can then be adjusted per-action.")
    minimum_volunteers = models.SmallIntegerField(
        default=1, help_text="minimum number of volunteers required for action")
    maximum_volunteers = models.SmallIntegerField(
        default=1, help_text="maximum number of volunteers required for action")


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('action type')
