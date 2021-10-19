from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.TextChoices):
    # Country.choices => [('AFG', 'Afghanistan'), ('AUS', 'Australia'), ...]
    # Country.AUSTRALIA.name => AUSTRALIA
    # Country.AUSTRALIA.label => Australia
    # Country.AUSTRALIA.value => AUS
    AFGHANISTAN = 'AFG', _('Afghanistan')
    AUSTRALIA = 'AUS', _('Australia')
    BRAZIL = 'BRA', _('Brazil')
    CHINA = 'CHN', _('China')
    FRANCE = 'FRA', _('France')


class Poll(models.Model):
    question = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    country = models.CharField(choices=Country.choices, max_length=3, default=Country.AFGHANISTAN)
    modified_by = models.ForeignKey(User, related_name='modified_by', on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("poll", "voted_by")
