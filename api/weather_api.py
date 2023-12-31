from typing import Optional, Annotated
import fastapi
from fastapi import Depends

from models.auth import User
from security.user import get_current_active_user
from models.location import Location
from models.validation_error import ValidationError
from services.openweather_service import get_report_async

router = fastapi.APIRouter()

@router.get('/api/weather/{city}')
async def weather(
        current_user: Annotated[User, Depends(get_current_active_user)],
        loc: Location = Depends(),
        units: Optional[str] = 'metric',
):
    try:
        
        forcast = await get_report_async(loc.city, loc.state, loc.country, units)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_message, status_code=ve.status_code)
    except Exception as e:
        print(f'server crashed while processing request: {e}')
        return fastapi.Response(content='Error proccessing your request.', status_code=500)
    return forcast
        