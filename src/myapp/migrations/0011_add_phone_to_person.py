from django.db import migrations

def add_phone_column(apps, schema_editor):
    vendor = schema_editor.connection.vendor

    if vendor == "sqlite":
        columns = [c.name for c in schema_editor.connection.introspection.get_table_description(
            schema_editor.connection.cursor(), "person"
        )]
        if "phone" not in columns:
            schema_editor.execute("ALTER TABLE person ADD COLUMN phone varchar(255);")

    elif vendor == "postgresql":
        schema_editor.execute("ALTER TABLE person ADD COLUMN IF NOT EXISTS phone varchar(255);")

    else:
        schema_editor.execute("ALTER TABLE person ADD COLUMN phone varchar(255);")

class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0010_add_age_to_person"),
    ]

    operations = [
        migrations.RunPython(add_phone_column, reverse_code=migrations.RunPython.noop),
    ]
