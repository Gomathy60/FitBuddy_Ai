from datetime import datetime
from sqlalchemy import Column,Integer,String,Float,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class User(Base):
 __tablename__='users'; id=Column(Integer,primary_key=True); user_id=Column(String(100),unique=True,index=True); name=Column(String(100)); age=Column(Integer); weight=Column(Float); goal=Column(String(100)); intensity=Column(String(20)); created_at=Column(DateTime,default=datetime.utcnow); plans=relationship('WorkoutPlan',back_populates='user',cascade='all, delete-orphan')
class WorkoutPlan(Base):
 __tablename__='workout_plans'; id=Column(Integer,primary_key=True); user_id=Column(Integer,ForeignKey('users.id')); original_plan=Column(Text); updated_plan=Column(Text); nutrition_tip=Column(Text); feedback=Column(Text); created_at=Column(DateTime,default=datetime.utcnow); user=relationship('User',back_populates='plans')
