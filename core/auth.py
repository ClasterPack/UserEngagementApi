import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.token_url)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Проверяет токен через внешний сервис авторизации.
    Делает HTTP запрос к auth сервису, получает данные пользователя.
    Если токен не валиден — возвращает 401.
    """
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{settings.auth_service_url}", headers=headers)
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authorization service unavailable",
            )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return response.json()
