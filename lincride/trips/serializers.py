from rest_framework import serializers

from trips import enums as trip_enums

from pricing import models as pricing_models
from pricing import enums as pricing_enums

class GetQuoteSerializer(serializers.Serializer):

    distance = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    demand_level = serializers.CharField(required=True)
    traffic_level = serializers.CharField(required=True)

    def get_quote(self, demand_level, traffic_level, distance):

        # validate parameters
        if demand_level in trip_enums.NULL_VALUES or demand_level.lower() not in [demand_level[0] for demand_level in pricing_enums.DEMAND_LEVELS]:
            return False, "oops! demand level cannot be empty - valid options are 'normal', 'peak'"
        
        if traffic_level in trip_enums.NULL_VALUES or traffic_level.lower() not in [traffic_level[0] for traffic_level in pricing_enums.TRAFFIC_LEVELS]:
            return False, "traffic level cannot be empty - valid options are 'low', 'normal', 'high'"
        
        if distance in [val for val in trip_enums.NULL_VALUES if val != 0]:
            return False, "distance cannot be empty"
                
        # get the pricing config for the demand_level and traffic_level
        try:
            pricing_config = pricing_models.PricingConfiguration.objects.get(demand_level=demand_level.lower(), traffic_level=traffic_level.lower())
        except Exception as get_pricing_config_error:
            # log error
            return False, "unable to fetch pricing configuration"
        
        is_quote, trip_quote = pricing_config.calculate_trip_quote(distance=distance, demand_level=demand_level, traffic_level=traffic_level)
        if not is_quote:
            return False, "unable to calculate trip quote"
        
        return True, trip_quote
        