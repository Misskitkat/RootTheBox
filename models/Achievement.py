# -*- coding: utf-8 -*-
"""
Created on Aug 11, 2013

@author: moloch

    Copyright 2012 Root the Box

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from builtins import str
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer, String, Unicode, DateTime

from models import dbsession
from models.BaseModels import DatabaseObject




class Achievement(DatabaseObject):
    """
    Achievement definition
    """

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    user = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint("user", "name"),
    )

    FLAG_ACH = "Captured their first Flag!"
    BOX_ACH = "Completed their first Box!"
    HINT_ACH = "Used their first Hint!"

    @classmethod
    def all(cls):
        """Returns a list of all objects in the database"""
        return dbsession.query(cls).all()
    
    @classmethod
    def by_id(cls, _id):
        """Returns a the object with id of _id"""
        return dbsession.query(cls).filter_by(id=_id).first()

    @classmethod
    def by_uuid(cls, _uuid):
        """Return and object based on a uuid"""
        return dbsession.query(cls).filter_by(uuid=str(_uuid)).first()
    
    @classmethod
    def by_user(cls, user):
        """Returns all achievements granted"""
        return dbsession.query(cls).filter_by(user=user.id).all()
    
    

def try_grant_achievement(user, ach_name) -> bool:
    user_achs = Achievement.by_user(user.id)
    if any(x.name == ach_name for x in user_achs):
        return False
    
    ach = Achievement()
    ach.user = user.id
    ach.name = ach_name
    dbsession.add(ach)
    dbsession.commit()

    return True
