# Generated by Django 2.2.5 on 2020-11-13 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_quizzes_lesson_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='newexammeeting',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]