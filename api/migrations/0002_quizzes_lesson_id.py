# Generated by Django 2.2.5 on 2020-11-12 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizzes',
            name='lesson_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Lesson'),
            preserve_default=False,
        ),
    ]
