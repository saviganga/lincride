from rest_framework import serializers

from pricing import models as pricing_models
from pricing import enums as pricing_enums

class PricingConfigurationSerializer(serializers.ModelSerializer):

    base_fare = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    cost_per_kilometer = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    traffic_level = serializers.CharField(required=True)
    demand_level = serializers.CharField(required=True)

    class Meta:
        model = pricing_models.PricingConfiguration
        fields = ["id", "demand_level", "traffic_level", "base_fare", "cost_per_kilometer", "created_at", "updated_at"]

    def create(self, validated_data):

        # validate the demand level
        if validated_data.get("demand_level").lower() not in [demand_level[0] for demand_level in pricing_enums.DEMAND_LEVELS]:
            return False, "oops! invalid demand level - valid options are 'normal', 'peak'"
        
        # validate the traffic level
        if validated_data.get("traffic_level").lower() not in [traffic_level[0] for traffic_level in pricing_enums.TRAFFIC_LEVELS]:
            return False, "oops! invalid traffic level - valid options are 'low', 'normal', 'high'"
        
        try:
            pricing_config = self.Meta.model.objects.create(**validated_data)
        except Exception as create_pricing_error:
            # log error
            
            return False, "Unable to create pricing configuration"
        
        return True, {
            "id": str(pricing_config.id),
            "demand_level": pricing_config.demand_level,
            "traffic_level": pricing_config.traffic_level,
            "base_fare": str(pricing_config.base_fare),
            "cost_per_kilometer": str(pricing_config.cost_per_kilometer),
            "created_at": str(pricing_config.created_at),
            "updated_at": str(pricing_config.updated_at)
        }
        
        