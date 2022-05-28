# Generated by Django 4.0.4 on 2022-05-25 06:08

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('home', '0004_homepagecarouselitem_read_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePastEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('event_title', models.CharField(blank=True, max_length=255, null=True)),
                ('event_body', models.TextField(blank=True, null=True)),
                ('event_date', models.CharField(blank=True, max_length=255, null=True)),
                ('event_location', models.CharField(blank=True, max_length=255, null=True)),
                ('event_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='past_events', to='home.homepage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
