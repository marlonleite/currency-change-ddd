from dataclasses import field
from datetime import datetime


class IdentityModel:
    id: int = field(init=False)
    updated_at: datetime = field(init=False)
    created_at: datetime = field(init=False)
