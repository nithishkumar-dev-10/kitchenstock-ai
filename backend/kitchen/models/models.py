from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from kitchen.core.database import Base
import uuid


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    # Profile
    family_size = Column(Integer, default=1)
    diet = Column(String, default="mixed")        # vegetarian / non-vegetarian / vegan / mixed
    region = Column(String, default="india")
    cooking_freq = Column(String, default="twice_daily")  # once / twice_daily / thrice / few_weekly

    # Onboarding flag
    onboarded = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    inventory = relationship("UserInventory", back_populates="user", cascade="all, delete")


class UserInventory(Base):
    __tablename__ = "user_inventory"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    item = Column(String, nullable=False)
    quantity = Column(Float, default=0.0)
    unit = Column(String, default="g")
    threshold = Column(Float, default=200.0)   # low stock trigger

    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship("User", back_populates="inventory")
