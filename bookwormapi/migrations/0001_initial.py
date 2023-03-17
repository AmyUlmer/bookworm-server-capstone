# Generated by Django 4.1.7 on 2023-03-17 16:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('released_date', models.DateField()),
                ('length', models.IntegerField()),
                ('description', models.CharField(max_length=150)),
                ('image_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=150)),
                ('date_of_event', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('max_capacity', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('image_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=150)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventReader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookwormapi.event')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookwormapi.reader')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(related_name='event_reader', through='bookwormapi.EventReader', to='bookwormapi.reader'),
        ),
        migrations.AddField(
            model_name='event',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_event', to='bookwormapi.book'),
        ),
        migrations.AddField(
            model_name='event',
            name='organizing_reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reader_event', to='bookwormapi.reader'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BookGenre_book', to='bookwormapi.bookgenre'),
        ),
        migrations.AddField(
            model_name='book',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reader_book', to='bookwormapi.reader'),
        ),
    ]
