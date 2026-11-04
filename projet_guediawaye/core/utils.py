from django.utils.text import slugify


def assign_unique_slug(instance, value, field_name="slug"):
    base_slug = slugify(value) or "element"
    slug = base_slug
    suffix = 2
    queryset = instance.__class__._default_manager

    while queryset.filter(**{field_name: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{suffix}"
        suffix += 1

    setattr(instance, field_name, slug)
