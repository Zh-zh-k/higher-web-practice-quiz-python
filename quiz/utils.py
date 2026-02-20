from django.shortcuts import get_object_or_404


def update_instance(model, instance_id, data):
    """Универсальное обновление модели по id."""
    instance = get_object_or_404(model, id=instance_id)

    for field, value in data.items():
        setattr(instance, field, value)

    instance.save()
    return instance
