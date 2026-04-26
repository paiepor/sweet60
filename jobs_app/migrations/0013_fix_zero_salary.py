from django.db import migrations

def fix_zero_salary(apps, schema_editor):
    # Already handled in 0012. This is a no-op kept for migration history continuity.
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('jobs_app', '0012_alter_joblisting_salary_and_more'),
    ]
    operations = [
        migrations.RunPython(fix_zero_salary),
    ]