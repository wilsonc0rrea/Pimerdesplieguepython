# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class ModuleBase(BaseModel):
    name: str
    label: str
    icon: str

class Module(ModuleBase):
    id: int
    class Config:
        from_attributes = True

class PermissionBase(BaseModel):
    module_id: int
    can_create: bool = False
    can_read: bool = True
    can_update: bool = False
    can_delete: bool = False

class PermissionCreate(PermissionBase):
    user_id: int

class PermissionOut(PermissionBase):
    id: int
    module: Module
    class Config:
        from_attributes = True

class UserPermissions(BaseModel):
    user_id: int
    username: str
    permissions: List[PermissionOut]