# backend/api/cases.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import CaseCreate, CaseUpdate, CaseResponse, MessageResponse
import crud

router = APIRouter()


@router.get("/cases", response_model=List[CaseResponse])
def list_cases(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    service: Optional[str] = Query(None, description="Filter by service name"),
    module: Optional[str] = Query(None, description="Filter by module name"),
    component: Optional[str] = Query(None, description="Filter by component name"),
    env: Optional[str] = Query(None, description="Filter by environment (uat, prod, etc.)"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve list of test cases with optional filters.

    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **service**: Filter by service (e.g., exchange_svc)
    - **module**: Filter by module (e.g., market)
    - **component**: Filter by component (e.g., candlestick)
    - **env**: Filter by environment (cases with empty environments match all)
    - **is_active**: Filter by active status (default: True)
    """
    cases = crud.get_cases(
        db,
        skip=skip,
        limit=limit,
        service=service,
        module=module,
        component=component,
        env=env,
        is_active=is_active
    )
    return cases


@router.get("/cases/{case_id}", response_model=CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single test case by ID.

    - **case_id**: Test case ID
    """
    case = crud.get_case_by_id(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case with id {case_id} not found")
    return case


@router.post("/cases", response_model=CaseResponse, status_code=201)
def create_case(case: CaseCreate, db: Session = Depends(get_db)):
    """
    Create a new test case (single-table design).

    Required fields:
    - **name**: Test case name
    - **service**: Service name
    - **test_config**: Complete test configuration in JSONB format
      - Must include 'steps' array (test steps)
      - Should include 'variables' dict (test data)
      - Should include 'validations' dict (validation rules)

    Optional fields:
    - **environments**: List of applicable environments (empty = all)
    - **jira_id**: Associated Jira ticket ID
    - **is_active**: Whether this test case is active (default: true)
    """
    try:
        # Validate test_config structure
        if 'steps' not in case.test_config:
            raise ValueError("test_config must contain 'steps' array")

        new_case = crud.create_case(db, case)
        return new_case
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create case: {str(e)}")


@router.put("/cases/{case_id}", response_model=CaseResponse)
def update_case(case_id: int, case: CaseUpdate, db: Session = Depends(get_db)):
    """
    Update an existing test case.

    - **case_id**: Test case ID
    - All fields from CaseCreate are accepted
    """
    updated_case = crud.update_case(db, case_id, case)
    if not updated_case:
        raise HTTPException(status_code=404, detail=f"Case with id {case_id} not found")
    return updated_case


@router.delete("/cases/{case_id}", response_model=MessageResponse)
def delete_case(case_id: int, db: Session = Depends(get_db)):
    """
    Delete a test case.

    - **case_id**: Test case ID
    """
    success = crud.delete_case(db, case_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Case with id {case_id} not found")
    return {"message": f"Case {case_id} deleted successfully"}


# ==================== Metadata Endpoints ====================

@router.get("/services", response_model=List[str])
def list_services(db: Session = Depends(get_db)):
    """
    Get list of all unique service names from existing test cases.
    Useful for populating filter dropdowns.
    """
    return crud.get_all_services(db)


@router.get("/modules", response_model=List[str])
def list_modules(db: Session = Depends(get_db)):
    """
    Get list of all unique module names from existing test cases.
    Useful for populating filter dropdowns.
    """
    return crud.get_all_modules(db)


@router.get("/components", response_model=List[str])
def list_components(db: Session = Depends(get_db)):
    """
    Get list of all unique component names from existing test cases.
    Useful for populating filter dropdowns.
    """
    return crud.get_all_components(db)
