from django.urls import path
from trips import views as trip_views

urlpatterns = [
    path("calculate-fare/", trip_views.GetQuoteView.as_view(), name="get-quote"),
]