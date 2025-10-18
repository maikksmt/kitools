from django.db import migrations


def normalize_scores(apps, schema_editor):
    Comparison = apps.get_model("compare", "Comparison")
    for obj in Comparison.objects.all():
        # Tools per historical model:
        tools_qs = obj.tools.all()
        if not tools_qs.exists():
            continue
        raw = obj.score_breakdown
        if not raw:
            continue

        # Minimale Inline-Normalisierung (historisches Modell: keine Methoden)
        tool_slugs = list(tools_qs.values_list("slug", flat=True))
        normalized = {}

        def split_pair(value):
            return [p.strip() for p in str(value).replace("：", ":").split(":")]

        if isinstance(raw, dict):
            for criterion, value in raw.items():
                row = {}
                if isinstance(value, dict):
                    # Mappe per slug, index fallback
                    for idx, slug in enumerate(tool_slugs):
                        v = value.get(slug)
                        if v is None:
                            v = value.get(str(idx)) or value.get(idx)
                        row[slug] = v if v not in (None, "", []) else "–"
                elif isinstance(value, (list, tuple)):
                    for idx, slug in enumerate(tool_slugs):
                        row[slug] = value[idx] if idx < len(value) else "–"
                else:
                    parts = split_pair(value)
                    for idx, slug in enumerate(tool_slugs):
                        row[slug] = parts[idx] if idx < len(parts) else "–"
                normalized[str(criterion)] = row
            obj.score_breakdown = normalized
            obj.save(update_fields=["score_breakdown"])


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("compare", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(normalize_scores, reverse_noop),
    ]
