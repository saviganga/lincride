from django.db import models
import uuid

from pricing import enums as api_enums

class PricingConfiguration(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cost_per_kilometer = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    base_fare = models.DecimalField(
        max_digits=100, decimal_places=2, default=0, help_text="Base fare for vehicle"
    )
    demand_level = models.CharField(
        max_length=10,
        choices=api_enums.DEMAND_LEVELS,
        default="normal",
    )
    traffic_level = models.CharField(
        max_length=10,
        choices=api_enums.DEMAND_LEVELS,
        default="normal",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("demand_level", "traffic_level")
        indexes = [
            models.Index(fields=["demand_level", "traffic_level"]),
        ]

    def __str__(self):
        return f"demand level: {self.demand_level} - traffic level: {self.traffic_level}"


