from typing import Optional
from pydantic import BaseModel


class DashboardVendorInfo(BaseModel):
    id: int
    name: str
    slug: str
    email: str
    is_active: bool


class DashboardSettingsInfo(BaseModel):
    business_start_hour: Optional[str] = None
    business_end_hour: Optional[str] = None
    off_hours_message: Optional[str] = None
    agent_enabled: bool = True
    tone: Optional[str] = None


class DashboardCatalogInfo(BaseModel):
    total_products: int
    knowledge_base_ready: bool


class DashboardOrdersInfo(BaseModel):
    total_orders: int
    pending_orders: int
    confirmed_orders: int
    processed_orders: int
    shipped_orders: int
    delivered_orders: int = 0
    cancelled_orders: int


class DashboardWhatsAppInfo(BaseModel):
    is_connected: bool
    phone_number_id: Optional[str] = None
    business_account_id: Optional[str] = None


class DashboardResponse(BaseModel):
    vendor: DashboardVendorInfo
    settings: DashboardSettingsInfo
    catalog: DashboardCatalogInfo
    orders: DashboardOrdersInfo
    whatsapp: DashboardWhatsAppInfo
