from django.db import models
from autoslug.fields import AutoSlugField


class Category(models.Model):
    category = models.CharField(max_length=100, blank=True, null=False)
    url = AutoSlugField(populate_from='category', unique=True, max_length=255)

    def get_absolute_url(self):
        return "/category/" + self.url

    def __str__(self):
        return self.category

    def __unicode__(self):
        return self.category


class Tour(models.Model):
    category = models.ForeignKey(Category, default=1, blank=True, null=True)
    title_PT = models.CharField(max_length=100, blank=True, null=False)
    title_EN = models.CharField(max_length=100, blank=True, null=False)
    title_DE = models.CharField(max_length=100, blank=True, null=False)
    description_PT = models.TextField(max_length=1000, blank=True, null=False)
    description_EN = models.TextField(max_length=1000, blank=True, null=False)
    description_DE = models.TextField(max_length=1000, blank=True, null=False)
    price = models.CharField(max_length=100, blank=True, null=False)
    img = models.FileField(null=True, blank=True)
    url = models.URLField(max_length=200, blank=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True, auto_created=False)
    keywords_SEO = models.TextField(max_length=2000, blank=True, null=False)
    description_SEO = models.TextField(max_length=2000, blank=True, null=False)
    position = models.IntegerField(default=1, blank=True, null=True)

    def get_absolute_url(self):
        return "/tours/%i/" % self.id

    def __str__(self):
        return self.title_EN

    def __unicode__(self):
        return self.title_EN

    class Meta:
        ordering = ["position", "-created_on"]


class Paragraph(models.Model):
    text_PT = models.TextField(max_length=500, blank=True, null=False)
    text_EN = models.TextField(max_length=500, blank=True, null=False)
    text_DE = models.TextField(max_length=500, blank=True, null=False)

    def __str__(self):
        return self.text_EN

    def __unicode__(self):
        return self.text_EN


class About(models.Model):
    paragraph = models.ManyToManyField(Paragraph)
    keywords_SEO = models.TextField(max_length=1000, blank=True, null=False)
    description_SEO = models.TextField(max_length=1000, blank=True, null=False)

    # def __str__(self):
    #     return self.paragraph

    def __unicode__(self):
        return self.paragraph
