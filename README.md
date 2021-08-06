# django-hashtag

## Installation

~~~
> pipenv install https://github.com/genosltd/django-hashtag
~~~

## Usage

Do not forget to list `django-hashtag` in `settings.py`, and make sure you also have `django.contrib.contenttypes` listed:

~~~python
# settings.py
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django_hashtag',
]
~~~

### Models

For models you declare, please use `TaggedItemBase` as your super class:

~~~python
# models.py
from django_hashtag import models as dht_models

class AModel(dht_models.TaggedItemBase):
    pass
~~~

With it you gain `hashtags` property returning Many2ManyField:

~~~
>>> a_model = AModel.objects.create()
>>> a_model.hashtags
<django.db.models.fields.{...}.ManyRelatedManager object at ...>

>>> python = a_model.hashtags.create(hashtag='python')
>>> guido = a_model.hashtags.create(hashtag='guido')
>>> a_model.hashtags.all()
<QuerySet [<Hashtag: #python>, <Hashtag: #guido>]>
~~~

### Admin

For admin interface, please use `TaggedItemBaseAdmin` as you super class:

~~~python
# admin.py
from django import admin
from django_hashtag import admin as dht_admin

from . import models


@admin.register(models.AModel)
class AModelAdmin(dht_admin.TaggedItemBaseAdmin):
    pass
~~~
