from fastapi import APIRouter
from server.services.policy_service import PolicyService

router = APIRouter()


@router.get("/policy")
async def policy():
    return PolicyService().policy()
