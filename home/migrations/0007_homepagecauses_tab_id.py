# Generated by Django 4.0.4 on 2022-05-28 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_givepage_givepagegalleryimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagecauses',
            name='tab_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
