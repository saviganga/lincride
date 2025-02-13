from django.test import TestCase
from decimal import Decimal
from pricing import models as pricing_models
from pricing import enums as pricing_enums
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status



class PricingConfigurationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.base_fare = Decimal("500.00")
        self.cost_per_km = Decimal("50.00")

        # Create different pricing configurations
        self.normal_low = pricing_models.PricingConfiguration.objects.create(
            demand_level="normal",
            traffic_level="low",
            base_fare=self.base_fare,
            cost_per_kilometer=self.cost_per_km,
        )

        self.normal_normal = pricing_models.PricingConfiguration.objects.create(
            demand_level="normal",
            traffic_level="normal",
            base_fare=self.base_fare,
            cost_per_kilometer=self.cost_per_km,
        )

        self.normal_high = pricing_models.PricingConfiguration.objects.create(
            demand_level="normal",
            traffic_level="high",
            base_fare=self.base_fare,
            cost_per_kilometer=self.cost_per_km,
        )

        self.peak_low = pricing_models.PricingConfiguration.objects.create(
            demand_level="peak",
            traffic_level="low",
            base_fare=self.base_fare,
            cost_per_kilometer=self.cost_per_km,
        )

        self.peak_normal = pricing_models.PricingConfiguration.objects.create(
            demand_level="peak",
            traffic_level="normal",
            base_fare=self.base_fare,
            cost_per_kilometer=self.cost_per_km,
        )

        self.peak_high = pricing_models.PricingConfiguration.objects.create(
            demand_level="peak",
            traffic_level="high",
            base_fare=self.base_fare,
            cost_per_kilometer=self.cost_per_km,
        )

    def test_normal_low_pricing(self):
        """normal demand & low traffic"""
        is_quote, quote = self.normal_low.calculate_trip_quote(distance=Decimal("10"), demand_level="normal", traffic_level="low")
        expected_fare = self.base_fare + (self.cost_per_km * Decimal("10"))
        
        self.assertTrue(is_quote)
        self.assertEqual(Decimal(quote["total_fare"]), expected_fare)

    def test_normal_normal_pricing(self):
        """normal demand & normal traffic"""
        is_quote, quote = self.normal_normal.calculate_trip_quote(distance=Decimal("10"), demand_level="normal", traffic_level="normal")
        expected_fare = self.base_fare + (self.cost_per_km * Decimal("10"))
        
        self.assertTrue(is_quote)
        self.assertEqual(Decimal(quote["total_fare"]), expected_fare)

    def test_normal_high_pricing(self):
        """normal demand & high traffic"""
        is_quote, quote = self.normal_high.calculate_trip_quote(distance=Decimal("10"), demand_level="normal", traffic_level="high")
        base_fare = self.base_fare + (self.cost_per_km * Decimal("10"))
        expected_fare = base_fare * (1 + Decimal(pricing_enums.MULTIPLIERS["traffic"]))
        
        self.assertTrue(is_quote)
        self.assertEqual(Decimal(quote["total_fare"]), expected_fare)

    def test_peak_low_pricing(self):
        """peak demand & low traffic"""
        is_quote, quote = self.peak_low.calculate_trip_quote(distance=Decimal("10"), demand_level="peak", traffic_level="low")
        base_fare = self.base_fare + (self.cost_per_km * Decimal("10"))
        expected_fare = base_fare * (1 + Decimal(pricing_enums.MULTIPLIERS["demand"]))
        
        self.assertTrue(is_quote)
        self.assertEqual(Decimal(quote["total_fare"]), expected_fare)

    def test_peak_normal_pricing(self):
        """peak demand & normal traffic"""
        is_quote, quote = self.peak_normal.calculate_trip_quote(distance=Decimal("10"), demand_level="peak", traffic_level="normal")
        base_fare = self.base_fare + (self.cost_per_km * Decimal("10"))
        expected_fare = base_fare * (1 + Decimal(pricing_enums.MULTIPLIERS["demand"]))
        
        self.assertTrue(is_quote)
        self.assertEqual(Decimal(quote["total_fare"]), expected_fare)

    def test_peak_high_pricing(self):
        """peak demand & high traffic"""
        is_quote, quote = self.peak_normal.calculate_trip_quote(distance=Decimal("10"), demand_level="peak", traffic_level="high")
        base_fare = self.base_fare + (self.cost_per_km * Decimal("10"))
        expected_fare = base_fare * (1 + Decimal(pricing_enums.MULTIPLIERS["demand"]))
        expected_fare = expected_fare * (1 + Decimal(pricing_enums.MULTIPLIERS["traffic"]))
        
        self.assertTrue(is_quote)
        self.assertEqual(Decimal(quote["total_fare"]), expected_fare)

    def test_valid_quote_normal_low(self):
        """valid api for quote calculation with normal demand and low traffic."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "demand_level": "normal", "traffic_level": "low"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_fare", response.data["data"])

    def test_valid_quote_normal_normal(self):
        """valid api for quote calculation with normal demand and normal traffic."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "demand_level": "normal", "traffic_level": "normal"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_fare", response.data["data"])

    def test_valid_quote_normal_high(self):
        """valid api for quote calculation with normal demand and high traffic."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "demand_level": "normal", "traffic_level": "high"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_fare", response.data["data"])

    def test_valid_quote_peak_low(self):
        """valid api for quote calculation with peak demand and low traffic."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "demand_level": "peak", "traffic_level": "low"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_fare", response.data["data"])

    def test_valid_quote_peak_normal(self):
        """valid api for quote calculation with peak demand and normal traffic."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "demand_level": "peak", "traffic_level": "normal"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_fare", response.data["data"])

    def test_valid_quote_peak_high(self):
        """valid api for quote calculation with peak demand and high traffic."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "demand_level": "peak", "traffic_level": "high"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_fare", response.data["data"])

    def test_invalid_demand_level(self):
        """error response for an invalid demand level."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "demand_level": "invalid", "traffic_level": "low"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("oops! demand level cannot be empty", response.data["message"])

    def test_invalid_traffic_level(self):
        """error response for an invalid traffic level."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "demand_level": "normal", "traffic_level": "invalid"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("traffic level cannot be empty", response.data["message"])

    def test_missing_distance(self):
        """error response for missing distance parameter."""
        response = self.client.get(
            reverse("get-quote"),
            {"demand_level": "normal", "traffic_level": "low"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("distance: This field is required.", response.data["message"])

    def test_missing_demad_level(self):
        """error response for missing demand level parameter."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "traffic_level": "low"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("demand_level: This field is required.", response.data["message"])

    def test_missing_traffic_level(self):
        """error response for missing traffic level parameter."""
        response = self.client.get(
            reverse("get-quote"),
            {"demand_level": "normal", "distance": "10"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("traffic_level: This field is required.", response.data["message"])

    def test_blank_distance(self):
        """error response for blank distance parameter."""
        response = self.client.get(
            reverse("get-quote"),
            {"demand_level": "normal", "traffic_level": "low", "distance": ""},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("distance: A valid number is required.", response.data["message"])

    def test_blank_demad_level(self):
        """error response for blank demand level parameter."""
        response = self.client.get(
            reverse("get-quote"),
            {"distance": "10", "traffic_level": "low", "demand_level": ""},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("demand_level: This field may not be blank.", response.data["message"])

    def test_blank_traffic_level(self):
        """error response for blank traffic level parameter."""
        response = self.client.get(
            reverse("get-quote"),
            {"demand_level": "normal", "distance": "10", "traffic_level": ""},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("traffic_level: This field may not be blank.", response.data["message"])

    

    
