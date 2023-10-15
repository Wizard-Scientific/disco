import csv
import pandas as pd
import logging

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, event
from sqlalchemy.orm import backref, relationship

from . import Base, db_session, engine
from .utils.crudmixin import CRUDMixin


class ChannelMetrics(Base, CRUDMixin):
    __tablename__ = "channel_metrics"
    id = Column(Integer, primary_key = True, nullable=False, autoincrement=True)

    timestamp = Column(DateTime)

    member_count = Column(Integer)
    online_count = Column(Integer)

    guild_id = Column(Integer, ForeignKey('guild.id'))
    guild = relationship('Guild', backref=backref('channel_metrics', lazy='dynamic'), foreign_keys=guild_id)

    def __repr__(self):
        return f"ChannelMetrics(timestamp={self.timestamp}, guild={self.guild}, member_count={self.member_count}, online_count={self.online_count})"

    @classmethod
    def get_timeseries(cls, guild, duration="1h"):
        if duration in ["1h"]:
            interval = 1 * 6
        elif duration in ["1d", "24h"]:
            interval = 24 * 6
        elif duration in ["1w", "7d"]:
            interval = 24 * 7 * 6

        sql = cls.query(guild=guild).order_by(cls.id.desc()).limit(interval).statement
        tmp_df = pd.read_sql(sql, db_session.bind)

        tmp_df["timestamp"] = pd.to_datetime(tmp_df["timestamp"]).apply(lambda x: x.replace(second=0, microsecond=0))

        tmp_df = tmp_df.sort_values(by="id", ascending=True)

        return tmp_df
