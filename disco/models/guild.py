import csv
import time
import requests
import datetime
import threading
import random
import json
import logging

import pandas as pd

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, event
from sqlalchemy.orm import backref, relationship

from . import Base, db_session
from .utils.crudmixin import CRUDMixin


class Guild(Base, CRUDMixin):
    __tablename__ = "guild"
    id = Column(Integer, primary_key = True, nullable=False)

    name = Column(String)

    def __repr__(self):
        return f"Guild(id={self.id}, name='{self.name}')"
