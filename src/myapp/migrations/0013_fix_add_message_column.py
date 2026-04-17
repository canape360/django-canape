from django.db import migrations

def add_message_column(apps, schema_editor):
    vendor = schema_editor.connection.vendor  # 'postgresql' or 'sqlite' etc.

    if vendor == "postgresql":
        schema_editor.execute('ALTER TABLE "myapp_mymail" ADD COLUMN IF NOT EXISTS "message" text;')

    elif vendor == "sqlite":
        # SQLiteは IF NOT EXISTS が使えないので、存在チェックしてから追加
        # PRAGMA table_info returns rows: cid, name, type, notnull, dflt_value, pk
        cursor = schema_editor.connection.cursor()
        cursor.execute('PRAGMA table_info("myapp_mymail");')
        cols = [row[1] for row in cursor.fetchall()]
        if "message" not in cols:
            schema_editor.execute('ALTER TABLE "myapp_mymail" ADD COLUMN "message" text;')

    else:
        # 他DBの場合は必要に応じて追加
        schema_editor.execute('ALTER TABLE "myapp_mymail" ADD COLUMN "message" text;')

def drop_message_column(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == "postgresql":
        schema_editor.execute('ALTER TABLE "myapp_mymail" DROP COLUMN IF EXISTS "message";')
    # SQLiteは DROP COLUMN が古いバージョンだと厳しいので、reverseは何もしない
    # （どうしても必要ならテーブル再作成が必要）

class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0012_add_address_to_person"),
    ]

    operations = [
        migrations.RunPython(add_message_column, drop_message_column),
    ]
