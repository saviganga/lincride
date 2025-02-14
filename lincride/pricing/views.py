from django.shortcuts import render


from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.decorators import action

from pricing import models as pricing_models
from pricing import serializers as pricing_serializers
from pricing.responses import u_responses
from pricing import utils as pricing_utls


class PricingConfigurationViewSet(ModelViewSet):
   
    queryset = pricing_models.PricingConfiguration.objects.all()
    serializer_class = pricing_serializers.PricingConfigurationSerializer

    def get_queryset(self):
        
        return self.queryset.all()
    
    def create(self, request, *args, **kwargs):
        
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:

            # log error
            return Response(
                data=u_responses.error_response(message=pricing_utls.handle_serializer_errors(serializer_error=serializer.errors)),
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_pricing, pricing_config = serializer.create(validated_data=serializer.validated_data)
        if not is_pricing:
            return Response(
                data=u_responses.error_response(message=pricing_config),
                status=status.HTTP_400_BAD_REQUEST,
            )
                
        success_response = {"message": "Pricing created successfully", "data": pricing_config}
        return Response(
            data=u_responses.success_response(data=success_response),
            status=status.HTTP_201_CREATED,
        )
    
    def list(self, request, *args, **kwargs):

        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.serializer_class(queryset, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True)
            success_response = {
                "message": "Successfully fetched pricing configurations",
                "data": serializer.data
            }
            
            return Response(
                    data=u_responses.success_response(data=success_response),
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                data=u_responses.error_response(message="Unable to fetch pricing configurations"),
                status=status.HTTP_400_BAD_REQUEST,
            )
