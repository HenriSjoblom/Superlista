from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_lists')

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    def share_list(self, user):
        self.shared_with.add(user)

    @staticmethod
    def get_shared_lists(user):
        return List.objects.filter(shared_with=user)

    @property
    def name(self):
        return self.item_set.first().text


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text
