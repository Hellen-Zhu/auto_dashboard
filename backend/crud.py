# backend/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from models import ApiAutoCase, Environment
from schemas import CaseCreate, CaseUpdate


# ==================== Test Case CRUD Operations ====================

def get_cases(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    service: Optional[str] = None,
    module: Optional[str] = None,
    component: Optional[str] = None,
    env: Optional[str] = None,
    is_active: Optional[bool] = True
) -> List[ApiAutoCase]:
    """
    Retrieve list of test cases with optional filters.

    Args:
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        service: Filter by service name
        module: Filter by module name
        component: Filter by component name
        env: Filter by environment (cases with empty environments array match all)
        is_active: Filter by active status (default: True, None = all)

    Returns:
        List of test cases
    """
    query = db.query(ApiAutoCase)

    # Filter by active status
    if is_active is not None:
        query = query.filter(ApiAutoCase.is_active == is_active)

    # Filter by service, module, component
    if service:
        query = query.filter(ApiAutoCase.service == service)
    if module:
        query = query.filter(ApiAutoCase.module == module)
    if component:
        query = query.filter(ApiAutoCase.component == component)

    # Environment filter: match cases with empty environments OR cases that contain the specified env
    if env:
        query = query.filter(
            or_(
                ApiAutoCase.environments == None,
                ApiAutoCase.environments == [],
                ApiAutoCase.environments.any(env)
            )
        )

    return query.offset(skip).limit(limit).all()


def get_case_by_id(db: Session, case_id: int) -> Optional[ApiAutoCase]:
    """
    Retrieve a single test case by ID.

    Args:
        db: Database session
        case_id: Test case ID

    Returns:
        Test case object or None if not found
    """
    return db.query(ApiAutoCase).filter(ApiAutoCase.id == case_id).first()


def create_case(db: Session, case: CaseCreate) -> ApiAutoCase:
    """
    Create a new test case.

    Args:
        db: Database session
        case: Test case data

    Returns:
        Created test case object
    """
    db_case = ApiAutoCase(**case.model_dump())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case


def update_case(db: Session, case_id: int, case: CaseUpdate) -> Optional[ApiAutoCase]:
    """
    Update an existing test case.

    Args:
        db: Database session
        case_id: Test case ID
        case: Updated test case data

    Returns:
        Updated test case object or None if not found
    """
    db_case = get_case_by_id(db, case_id)
    if not db_case:
        return None

    for key, value in case.model_dump().items():
        setattr(db_case, key, value)

    db.commit()
    db.refresh(db_case)
    return db_case


def delete_case(db: Session, case_id: int) -> bool:
    """
    Delete a test case.

    Args:
        db: Database session
        case_id: Test case ID

    Returns:
        True if deleted, False if not found
    """
    db_case = get_case_by_id(db, case_id)
    if not db_case:
        return False

    db.delete(db_case)
    db.commit()
    return True


# ==================== Data Set CRUD Operations (DEPRECATED) ====================
# NOTE: These functions are kept for backward compatibility but are no longer used.
# The single-table design eliminates the need for separate dataset management.
# All test data is now stored in ApiAutoCase.test_config

# The following functions can be safely removed once all clients are migrated:
# - get_datasets_by_case()
# - get_dataset_by_id()
# - create_dataset()
# - update_dataset()
# - delete_dataset()


# ==================== Environment CRUD Operations ====================

def get_environments(db: Session) -> List[Environment]:
    """
    Retrieve all active environments.

    Args:
        db: Database session

    Returns:
        List of active environments
    """
    return db.query(Environment).filter(Environment.is_active == True).all()


# ==================== Metadata Operations ====================

def get_all_services(db: Session) -> List[str]:
    """
    Get list of all unique service names.

    Args:
        db: Database session

    Returns:
        List of service names
    """
    result = db.query(ApiAutoCase.service).distinct().all()
    return [r[0] for r in result if r[0]]


def get_all_modules(db: Session) -> List[str]:
    """
    Get list of all unique module names.

    Args:
        db: Database session

    Returns:
        List of module names
    """
    result = db.query(ApiAutoCase.module).distinct().all()
    return [r[0] for r in result if r[0]]


def get_all_components(db: Session) -> List[str]:
    """
    Get list of all unique component names.

    Args:
        db: Database session

    Returns:
        List of component names
    """
    result = db.query(ApiAutoCase.component).distinct().all()
    return [r[0] for r in result if r[0]]
