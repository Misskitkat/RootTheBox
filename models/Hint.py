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


import xml.etree.cElementTree as ET
from builtins import str
from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Unicode, DateTime

from libs.ValidationError import ValidationError
from models import dbsession
from models.BaseModels import DatabaseObject
from models.Box import Box
from models.Flag import Flag
from models.Relationships import team_to_hint


class Hint(DatabaseObject):

    """
    Holds the source code for a box which can be purchased from
    the source code market.
    """

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    box_id = Column(Integer, ForeignKey("box.id"), nullable=False)
    flag_id = Column(Integer, ForeignKey("flag.id"), nullable=True)
    _price = Column(Integer, nullable=False)
    _description = Column(Unicode(4096), nullable=False)
    _unlock_time = Column(DateTime, default=None, nullable=True)

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
        """Returns a the object with a given uuid"""
        return dbsession.query(cls).filter_by(uuid=str(_uuid)).first()

    @classmethod
    def by_box_id(cls, _id):
        return dbsession.query(cls).filter_by(box_id=_id).all()

    @classmethod
    def by_flag_id(cls, _id):
        return dbsession.query(cls).filter_by(flag_id=_id).all()

    @classmethod
    def taken_by_flag(cls, _id):
        return (
            dbsession.query(cls, team_to_hint)
            .filter_by(flag_id=_id)
            .join(team_to_hint)
            .all()
        )

    @classmethod
    def taken_by_box(cls, _id):
        return (
            dbsession.query(cls, team_to_hint)
            .filter_by(box_id=_id, flag_id=None)
            .join(team_to_hint)
            .all()
        )

    @property
    def flag(self):
        return Flag.by_id(self.flag_id)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        try:
            self._price = abs(int(value))
        except ValueError:
            raise ValidationError("Hint price must be an integer")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not 0 < len(value) < 4097:
            raise ValidationError("Hint description must be 1 - 4096 characters")
        self._description = str(value)

    @property
    def unlock_time(self):
        if self._unlock_time is None or self._unlock_time == "":
            return ""
        return self._unlock_time.strftime("%Y-%m-%dT%H:%M")

    @unlock_time.setter
    def unlock_time(self, time):
        if time and len(time) > 0:
            print(time)
            self._unlock_time = datetime.strptime(time, "%Y-%m-%dT%H:%M")
        else:
            self._unlock_time = None

    @property
    def is_unlocked(self):
        unlocked = self._unlock_time
        if unlocked and unlocked != "":
            return datetime.now() > unlocked
        return False
        
    def to_xml(self, parent):
        hint_elem = ET.SubElement(parent, "hint")
        ET.SubElement(hint_elem, "price").text = str(self.price)
        ET.SubElement(hint_elem, "description").text = self._description

    def to_dict(self):
        flag = Flag.by_id(self.flag_id)
        if flag:
            flag_uuid = flag.uuid
        else:
            flag_uuid = ""
        return {
            "price": str(self.price),
            "description": self.description,
            "flag_uuid": flag_uuid,
            "uuid": self.uuid,
            "flaglist": Box.flaglist(self.box_id),
        }
