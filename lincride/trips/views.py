from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from trips import serializers as trip_serializers

from pricing.responses import u_responses
from pricing import utils as pricing_utls

class GetQuoteView(APIView):

    def get(self, request):

        # valuidate the query params
        serializer = trip_serializers.GetQuoteSerializer(data=request.GET)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as serializer_error:
            return Response(
                data=u_responses.error_response(message=pricing_utls.handle_serializer_errors(serializer_error=serializer.errors)),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # get the query parameters
        demand_level = request.GET.get("demand_level", None)
        traffic_level = request.GET.get("traffic_level", None)
        distance = request.GET.get("distance", None)

        # calculate the quote
        is_quote, trip_quote = serializer.get_quote(demand_level=demand_level, traffic_level=traffic_level, distance=distance)
        if not is_quote:
            return Response(
                data=u_responses.error_response(message=trip_quote),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        success_response = {"message": "Successfully calculated trip quote", "data": trip_quote}
        return Response(
            data=u_responses.success_response(data=success_response),
            status=status.HTTP_200_OK,
        )