from django.db import migrations


GRUPO_CLIENTES = "Clientes"


def criar_grupo_clientes(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("auth", "User")

    grupo_clientes, _ = Group.objects.get_or_create(name=GRUPO_CLIENTES)
    usuarios_existentes = User.objects.filter(is_superuser=False)
    grupo_clientes.user_set.add(*usuarios_existentes)


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(criar_grupo_clientes, migrations.RunPython.noop),
    ]
