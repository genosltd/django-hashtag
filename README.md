# django-hashtag

## Installation

~~~
> pipenv install https://github.com/genosltd/django-hashtag
~~~

## Usage

Do not forget to list `django_hashtag` in `settings.py`, and make sure you also have `django.contrib.contenttypes` listed:

~~~python
# settings.py
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django_hashtag',
]
~~~

### Models

For models you declare, please use `HasHashtags` as your super class:

~~~python
# models.py
from django_hashtag.models import HasHashtags

class AModel(HasHashtags):
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

For admin interface, please use `HasHashtagsAdmin` as you super class:

~~~python
# admin.py
from django import admin
from django_hashtag.admin import HasHashtagsAdmin

from . import models


@admin.register(models.AModel)
class AModelAdmin(HasHashtagsAdmin):
    pass
~~~


### Testing

For testing please use:

~~~
> pipenv run tests\runtests.py
~~~

or with coverage:

~~~
> pipenv run coverage run --source django_hashtag tests\runtests.py
~~~

and then for html coverage report (in `htmlcov`):

~~~
> pipenv run coverage html
~~~
