# API Documentation


## APIs Overview

- **Base Url**: `127.0.0.1:8000`


### Pricing Configuration
Pricing configurations have to be set before users an check for quote calculations. The pricing configurations set depend on the traffic level and demand level

#### 1. Create Pricing Configuration
This endpoint allows users to create a new pricing configuration.

- **Endpoint**: `{{BASE_URL}}/pricing/`
- **Method**: POST

**Request Body:**
```json
{
    "traffic_level": "normal",
    "demand_level": "peak",
    "base_fare": "230",
    "cost_per_kilometer": "27"
}
```

#### 2. Get Pricing Configurations
This endpoint allows users to get oricing configurations.

- **Endpoint**: `{{BASE_URL}}/pricing/`
- **Method**: GET



### Quote
After the pricing configurations have been set, the user can check trip fares


#### 2. Get Pricing Configurations
This endpoint allows users to get oricing configurations.

- **Endpoint**: `{{BASE_URL}}/api/calculate-fare/?distance=<distance_value>&demand_level=<demand_level>&traffic_level=<traffic_level>`
- **Method**: GET
