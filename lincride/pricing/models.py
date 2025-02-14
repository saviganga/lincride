from django.db import models
import uuid
from decimal import Decimal

from pricing import enums as pricing_enums

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
        choices=pricing_enums.DEMAND_LEVELS,
        default="normal",
    )
    traffic_level = models.CharField(
        max_length=10,
        choices=pricing_enums.DEMAND_LEVELS,
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
    
    def calculate_trip_quote(self, distance, demand_level, traffic_level):

        # get the multipliers
        multipliers = pricing_enums.MULTIPLIERS

        # calculate cost per km
        cost_per_km = round((self.cost_per_kilometer * Decimal(distance)), 1)

        trip_quote_price = round((self.base_fare + cost_per_km), 1)

        # check demand and traffic levels
        if demand_level.lower() == "peak":
            demand_multiplier_value = Decimal(multipliers.get('demand'))
            trip_quote_price = round(((trip_quote_price * demand_multiplier_value) + trip_quote_price), 1)
        else:
            demand_multiplier_value = Decimal("0")
            trip_quote_price = trip_quote_price
        
        if traffic_level.lower() == 'high':
            traffic_multiplier_value = Decimal(multipliers.get('traffic'))
            trip_quote_price = round(((trip_quote_price * traffic_multiplier_value) + trip_quote_price), 1)
        else:
            traffic_multiplier_value = Decimal("0")
            trip_quote_price = trip_quote_price

        return True, {
            "base_fare": str(self.base_fare),
            "distance_fare": str(cost_per_km),
            "traffic_multiplier": str(traffic_multiplier_value),
            "demand_multiplier": str(demand_multiplier_value),
            "total_fare": str(trip_quote_price)
        }








