from django.db import migrations

def add_address_column(apps, schema_editor):
    vendor = schema_editor.connection.vendor

    if vendor == "sqlite":
        # SQLiteは IF NOT EXISTS が使えないので存在チェックしてから追加
        cols = [c.name for c in schema_editor.connection.introspection.get_table_description(
            schema_editor.connection.cursor(), "myapp_person"
        )]
        if "address" not in cols:
            schema_editor.execute("ALTER TABLE myapp_person ADD COLUMN address varchar(255);")

    elif vendor == "postgresql":
        schema_editor.execute("ALTER TABLE myapp_person ADD COLUMN IF NOT EXISTS address varchar(255);")

    else:
        schema_editor.execute("ALTER TABLE myapp_person ADD COLUMN address varchar(255);")

class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0011_add_phone_to_person"),
    ]

    operations = [
        migrations.RunPython(add_address_column, reverse_code=migrations.RunPython.noop),
    ]
