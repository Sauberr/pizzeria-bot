# Generated by Django 5.1.4 on 2025-01-29 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usersmanage", "0002_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "🕒 Pending"),
                    ("completed", "✅ Completed"),
                    ("cancelled", "❌ Cancelled"),
                ],
                default="pending",
                max_length=25,
            ),
        ),
    ]
