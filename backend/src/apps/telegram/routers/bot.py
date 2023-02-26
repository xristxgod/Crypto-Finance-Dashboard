from fastapi import APIRouter

from apps.telegram.bot.messanger import messanger

router = APIRouter()


@router.on_event('startup')
async def startup():
    # Create messanger
    await messanger.setup()
