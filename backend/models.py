# backend/models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from database import Base


class ApiAutoCase(Base):
    """
    Unified test case definition table (single-table design).
    Each row represents a complete, independent test case.

    The test_config JSONB column contains:
    - steps: List of test steps with HTTP/WebSocket actions
    - variables: Test data variables (previously in case_data_sets)
    - validations: Validation rules (previously validations_override)
    """
    __tablename__ = 'api_auto_cases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Classification fields
    service = Column(String(100), nullable=False, index=True)
    module = Column(String(100), index=True)
    component = Column(String(100), index=True)
    tags = Column(ARRAY(Text), index=True)

    # Environment targeting (moved from case_data_sets)
    environments = Column(ARRAY(Text), index=True)

    # External references
    jira_id = Column(String(50), unique=True)
    author = Column(String(50))

    # Core test configuration (consolidated from parameters + dataset variables)
    # Structure: {"steps": [...], "variables": {...}, "validations": {...}}
    test_config = Column(JSONB, nullable=False)

    # Status and metadata
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Environment(Base):
    """
    Test environment configuration table.
    Each row represents a specific service in a specific environment.

    Example rows:
    - (uat, exchange_svc, https://uat-api.3ona.co)
    - (uat, websocket_svc, wss://uat-stream.3ona.co)
    """
    __tablename__ = 'test_environments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)  # Environment name: dev, uat, prod
    service = Column(String(50), nullable=False, index=True)  # Service name
    base_url = Column(String(255), nullable=False)  # Service-specific base URL
    description = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
