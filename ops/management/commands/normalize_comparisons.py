from django.core.management.base import BaseCommand
from compare.models import Comparison


class Command(BaseCommand):
    help = "Normalizes score_breakdown of all comparisons to {criterion: {tool_slug: score}}"

    def handle(self, *args, **opts):
        n = 0
        for c in Comparison.objects.prefetch_related("tools"):
            if c.tools.exists() and c.score_breakdown:
                c.normalize_score_breakdown()
                c.save(update_fields=["score_breakdown"])
                n += 1
        self.stdout.write(self.style.SUCCESS(f"Normalized {n} comparison(s)."))
