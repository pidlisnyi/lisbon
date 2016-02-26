from django.db import models


class Tour(models.Model):
    title_pt = models.CharField(max_length=100, blank=True, null=False)
    title_en = models.CharField(max_length=100, blank=True, null=False)
    title_de = models.CharField(max_length=100, blank=True, null=False)
    text = models.TextField(max_length=1000, blank=True, null=False)
    url = models.URLField(max_length=200, blank=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True, auto_created=False)
    img = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title_pt

    def __unicode__(self):
        return self.title_pt


class Offer(models.Model):
    title = models.CharField(max_length=100, blank=True, null=False)
    text = models.TextField(max_length=1000, blank=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True, auto_created=False)
    img = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
