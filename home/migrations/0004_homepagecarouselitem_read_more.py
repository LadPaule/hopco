# Generated by Django 4.0.4 on 2022-05-25 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_aboutpage_contactpage_empoweringpage_refugespage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagecarouselitem',
            name='read_more',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]