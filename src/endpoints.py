import asyncio

from fastapi import APIRouter
from services.nba_clip_service import *

router = APIRouter()


@router.get("/get_nba_clips")
async def get_nba_clips(game_IDs):
    data = clip_endpoint(game_IDs)
    return data
