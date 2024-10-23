# OHGO Wrapper

This is a python package that provides a simple interface to the [OHGO API](https://publicapi.ohgo.com/). 

## Installation
```bash
pip install ohgo
```

## Examples
### Authentication
```python
from ohgo import OHGOClient

# Register with OHGo for an API Key (https://publicapi.ohgo.com/docs/registration)
client = OHGOClient(api_key='YOUR-API-KEY')
```

### Get Cameras (default page size is 500)
```python
cameras = client.get_cameras()
```

### Get All Cameras
```python
from ohgo.models import QueryParams
params = QueryParams(page_all=True)
cameras = client.get_cameras(params=params)
```

### Get Cameras by Filter
```python
from ohgo.models import QueryParams
from ohgo.types import Region
params = QueryParams(county=Region.COLUMBUS, page_size=10, page=2)
cameras = client.get_cameras(params=params)
```

### Get Camera by ID
```python
camera = client.get_camera(camera_id='YOUR-CAMERA-ID')
```

### Get Images from Camera
```python
camera = client.get_camera(camera_id='YOUR-CAMERA-ID')
images = client.get_images(camera, "small") # Returns [ Image, Image, ... ]

# OR 
camera_view = camera.camera_views[0]
images = client.get_image(camera_view, "small") # Returns Image
```

### Other Endpoints
```python
client.get_digital_signs() # -> List[DigitalSign]
client.get_constructions() # -> List[Construction]
client.get_weather_sensor_sites() # -> List[WeatherSensorSite]
client.get_incidents() # -> List[Incident]
client.get_dangerous_slowdowns() # -> List[DangerousSlowdown]
client.get_travel_delays() # -> List[TravelDelay]
client.get_cameras() # -> List[Camera]
```

### Other Query Objects
```python
from ohgo.models import QueryParams, DigitalSignParams, ConstructionParams, WeatherSensorSiteParams
from ohgo.types import Region, SignType
import datetime
    
# Note: If you use *all* these params you will probably get no results
params = QueryParams(page_size=10, page=2, region=Region.COLUMBUS, map_bounds_sw=(39.9612, -82.9988), map_bounds_ne=(40.0150, -82.8874), radius=(39.9612, -82.9988, 10))
digital_sign_params = DigitalSignParams(sign_type=SignType.DMS)
    
# You can use string in the format 'YYYY-MM-DD', but it is recommended to use datetime objects
construction_params = ConstructionParams(include_future=datetime.datetime.now(), future_only=datetime.datetime.now())
weather_sensor_site_params = WeatherSensorSiteParams(hazards_only=True)

# All params inherit default attributes from QueryParams
```

### Cacheing Responses (ETag)
For convenience, the OHGo API supports ETag headers. If you pass an etag value in the request, 
the API will return an empty list if there are no changes since the last request. 
This can be useful for reducing the number of requests made to the API. This applies to all endpoints.

```python
cameras = client.get_cameras() # -> Technically returns CameraListResult object
etag = cameras.etag # -> Store this etag value and pass it in the next request
new_cameras = client.get_cameras(etag=etag) # -> Returns empty list if no changes since last request
cached = new_cameras.cached # -> True if the response was cached
if (cached):
    # use your original set of data
    return cameras
else:
    # use the new set of data
    return new_cameras
```
