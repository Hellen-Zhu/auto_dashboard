# backend/api/datasets.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import DataSetCreate, DataSetUpdate, DataSetResponse, MessageResponse
import crud

router = APIRouter()


@router.get("/cases/{case_id}/datasets", response_model=List[DataSetResponse])
def list_datasets(case_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all data sets for a specific test case.

    - **case_id**: Parent test case ID
    """
    # Verify case exists
    case = crud.get_case_by_id(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case with id {case_id} not found")

    datasets = crud.get_datasets_by_case(db, case_id)
    return datasets


@router.get("/datasets/{dataset_id}", response_model=DataSetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single data set by ID.

    - **dataset_id**: Data set ID
    """
    dataset = crud.get_dataset_by_id(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset with id {dataset_id} not found")
    return dataset


@router.post("/datasets", response_model=DataSetResponse, status_code=201)
def create_dataset(dataset: DataSetCreate, db: Session = Depends(get_db)):
    """
    Create a new data set for a test case.

    Required fields:
    - **case_id**: Parent test case ID
    - **data_set_name**: Data set name
    - **variables**: Test data variables in JSON format

    Optional fields:
    - **validations_override**: Override validation rules
    - **environments**: Applicable environments (empty = all)
    - **jira_id**: Associated Jira ticket ID
    - **is_active**: Whether this data set is active (default: true)
    """
    # Verify case exists
    case = crud.get_case_by_id(db, dataset.case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case with id {dataset.case_id} not found")

    try:
        new_dataset = crud.create_dataset(db, dataset)
        return new_dataset
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create dataset: {str(e)}")


@router.put("/datasets/{dataset_id}", response_model=DataSetResponse)
def update_dataset(dataset_id: int, dataset: DataSetUpdate, db: Session = Depends(get_db)):
    """
    Update an existing data set.

    - **dataset_id**: Data set ID
    - All fields from DataSetCreate are accepted (except case_id)
    """
    updated_dataset = crud.update_dataset(db, dataset_id, dataset)
    if not updated_dataset:
        raise HTTPException(status_code=404, detail=f"Dataset with id {dataset_id} not found")
    return updated_dataset


@router.delete("/datasets/{dataset_id}", response_model=MessageResponse)
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """
    Delete a data set.

    - **dataset_id**: Data set ID
    """
    success = crud.delete_dataset(db, dataset_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Dataset with id {dataset_id} not found")
    return {"message": f"Dataset {dataset_id} deleted successfully"}
