# backend/schemas.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


# ==================== Test Case Schemas ====================

class CaseBase(BaseModel):
    """Base schema for test case with common fields (single-table design)"""
    name: str = Field(..., description="Test case name")
    description: Optional[str] = Field(None, description="Test case description")
    service: str = Field(..., description="Service name (e.g., exchange_svc)")
    module: Optional[str] = Field(None, description="Module name (e.g., market)")
    component: Optional[str] = Field(None, description="Component name (e.g., candlestick)")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization (e.g., P0, smoke)")
    environments: Optional[List[str]] = Field(None, description="Applicable environments (e.g., uat, prod). Empty = all environments")
    jira_id: Optional[str] = Field(None, description="Associated Jira ticket ID")
    author: Optional[str] = Field(None, description="Test case author")
    test_config: Dict[str, Any] = Field(
        ...,
        description="Complete test configuration containing: steps (list), variables (dict), validations (dict)"
    )
    is_active: bool = Field(True, description="Whether this test case is active")


class CaseCreate(CaseBase):
    """Schema for creating a new test case"""
    pass


class CaseUpdate(CaseBase):
    """Schema for updating an existing test case"""
    pass


class CaseResponse(CaseBase):
    """Schema for test case response"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseListItem(BaseModel):
    """Simplified schema for test case list view"""
    id: int
    name: str
    service: str
    module: Optional[str]
    component: Optional[str]
    tags: Optional[List[str]]
    environments: Optional[List[str]]
    jira_id: Optional[str]
    is_active: bool
    created_at: datetime
    steps_count: int = Field(0, description="Number of test steps")

    model_config = ConfigDict(from_attributes=True)


# ==================== Data Set Schemas (DEPRECATED - For backward compatibility only) ====================
# NOTE: These schemas are kept for backward compatibility but are no longer used.
# The single-table design consolidates all data into ApiAutoCase.test_config

class DataSetBase(BaseModel):
    """DEPRECATED: Base schema for data set with common fields"""
    data_set_name: str = Field(..., description="Data set name")
    variables: Dict[str, Any] = Field(..., description="Test data variables in JSON format")
    validations_override: Optional[Dict[str, Any]] = Field(None, description="Override validation rules")
    environments: Optional[List[str]] = Field(None, description="Applicable environments (empty = all)")
    jira_id: Optional[str] = Field(None, description="Associated Jira ticket ID")
    is_active: bool = Field(True, description="Whether this data set is active")


class DataSetCreate(DataSetBase):
    """DEPRECATED: Schema for creating a new data set"""
    case_id: int = Field(..., description="Parent test case ID")


class DataSetUpdate(DataSetBase):
    """DEPRECATED: Schema for updating an existing data set"""
    pass


class DataSetResponse(DataSetBase):
    """DEPRECATED: Schema for data set response"""
    id: int
    case_id: int

    model_config = ConfigDict(from_attributes=True)


# ==================== Environment Schemas ====================

class EnvironmentResponse(BaseModel):
    """Schema for environment configuration response"""
    id: int
    name: str = Field(..., description="Environment name (e.g., dev, uat, prod)")
    service: str = Field(..., description="Service name")
    base_url: str = Field(..., description="Service base URL")
    description: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ==================== Utility Schemas ====================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
