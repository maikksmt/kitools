from django.core.exceptions import ValidationError
from django.db import models
from catalog.models import Tool
from django.utils.translation import gettext_lazy as _


class Comparison(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    intro = models.TextField(blank=True)
    tools = models.ManyToManyField(Tool, related_name='comparisons', blank=True)
    score_breakdown = models.JSONField(default=dict, blank=True)  # {tool_slug: {kriterium: score}}
    winner = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        verbose_name = 'Vergleich'
        verbose_name_plural = 'Vergleiche'

    def __str__(self):
        return self.title

    def _tool_slugs_in_order(self):
        """
        Liefert die Tool-Slugs in deterministischer Reihenfolge für Mapping
        (Reihenfolge = aktuelle .tools.all()-Reihenfolge).
        """
        return [getattr(t, "slug", str(t.pk)) for t in self.tools.all()]

    @staticmethod
    def _split_pair_string(value):
        """
        Akzeptiert Strings wie "9:8" oder "9 : 8" → ["9","8"].
        """
        if value is None:
            return []
        parts = str(value).replace("：", ":").split(":")
        return [p.strip() for p in parts]

    def normalize_score_breakdown(self):
        """
        Normalisiert self.score_breakdown in das Ziel-Format:
        {criterion: {tool_slug: score, ...}, ...}
        Unterstützt Eingangsdaten:
          - dict[str, dict[str, Any]]  (Keys = slug|name|pk|index)
          - dict[str, str]             (z.B. "9 : 8")
          - dict[str, list]            (z.B. ["9","8"])
        Nutzt die Reihenfolge der verknüpften Tools.
        """
        raw = self.score_breakdown or {}
        if not isinstance(raw, dict):
            # Irgendwas anderes → leeren, um Fehler zu vermeiden
            self.score_breakdown = {}
            return

        tool_slugs = self._tool_slugs_in_order()
        normalized = {}

        for criterion, value in raw.items():
            row = {}
            if isinstance(value, dict):
                # Versuche verschiedene Schlüsseltypen aufzulösen
                for idx, slug in enumerate(tool_slugs):
                    # Kandidaten: slug, name, pk, index
                    # Name/Pk holen wir nur, wenn sie tatsächlich existieren
                    row[slug] = (
                            value.get(slug) or
                            # Wir kennen das Tool-Objekt noch nicht hier, deshalb nur generische Keys:
                            value.get(str(idx)) or
                            value.get(idx)  # falls jemand integer keys gesetzt hat
                    )
                    # Falls leer, später "–"
            elif isinstance(value, (list, tuple)):
                for idx, slug in enumerate(tool_slugs):
                    row[slug] = value[idx] if idx < len(value) else None
            else:
                # String "9 : 8"
                parts = self._split_pair_string(value)
                for idx, slug in enumerate(tool_slugs):
                    row[slug] = parts[idx] if idx < len(parts) else None

            # Leerwerte auf "–" setzen
            for slug in tool_slugs:
                v = row.get(slug, None)
                row[slug] = "–" if v in (None, "", []) else v

            normalized[str(criterion)] = row

        self.score_breakdown = normalized

    def clean(self):
        """
        Validierung vor dem Speichern: Tools müssen vorhanden sein, wenn score_breakdown gesetzt wird.
        """
        super().clean()
        if self.score_breakdown:
            if self.pk is None and not self.id and self.tools.count() == 0:
                # Bei neuem Objekt kann M2M noch leer sein — Validierung erfolgt dann im save() nach m2m_set
                return
            if self.tools.count() == 0:
                raise ValidationError({"tools": _("Mindestens ein Tool wird für den Score-Vergleich benötigt.")})

    def save(self, *args, **kwargs):
        """
        Beim Speichern normalisieren. Achtung: Bei einem frisch erstellten Objekt existieren M2M noch nicht,
        deshalb normalisieren wir hier nur, wenn Tools bereits gesetzt sind.
        """
        # Erst regulär speichern, damit M2M später gesetzt werden kann
        super().save(*args, **kwargs)
        # Nach dem ersten Save: falls Tools vorhanden → normalisieren + erneut speichern (nur JSON-Feld ändert sich)
        if self.tools.exists():
            self.normalize_score_breakdown()
            super().save(update_fields=["score_breakdown"])
