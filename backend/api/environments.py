# backend/api/environments.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import EnvironmentResponse
import crud

router = APIRouter()


@router.get("/environments", response_model=List[EnvironmentResponse])
def list_environments(db: Session = Depends(get_db)):
    """
    Retrieve all active test environments.

    Returns list of environment configurations including:
    - Environment name (dev, uat, prod)
    - Service name
    - Base URL for the service
    - Description
    - Active status
    """
    environments = crud.get_environments(db)
    return environments
