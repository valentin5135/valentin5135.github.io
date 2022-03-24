from django.db import models


class Articles(models.Model):
    title = models.CharField('article title', max_length=100)
    content = models.TextField('article text')

    def __str__(self):
        return self.title

class Search(models.Model):
    search_page = models.CharField('search Encyclopedia', max_length=100)

    def __str__(self):
        return self.search_page
