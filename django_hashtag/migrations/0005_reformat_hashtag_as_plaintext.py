# Generated by Django 3.1.13 on 2021-08-18 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_hashtag', '0004_hahstags_related_name_rename_to_tagged_items'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hashtag',
            options={},
        ),
        migrations.AlterModelOptions(
            name='taggeditem',
            options={'verbose_name': 'hashtag'},
        ),
        migrations.AlterField(
            model_name='hashtag',
            name='hashtag',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='taggeditem',
            name='hashtags',
            field=models.ManyToManyField(blank=True, related_name='taggeditems', to='django_hashtag.Hashtag'),
        ),
    ]
