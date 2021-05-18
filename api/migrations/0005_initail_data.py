from __future__ import unicode_literals
from django.db import models, migrations

def load_from_sql():
    from django.conf import settings
    import os
    sql_statements = open(os.path.join(settings.BASE_DIR,'api/sql/initialdata.sql'), 'r').read()
    return sql_statements

# def delete_with_sql():
#     return 'DELETE from stores_store;'

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]
    operations = [
        migrations.RunSQL(load_from_sql()),
    ]
