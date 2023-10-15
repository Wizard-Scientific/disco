import pytest
import datetime

from pprint import pprint

from disco.models import Guild, ChannelMetrics


def test_channel_metrics_create():
    g = Guild.find(name="")
    c = ChannelMetrics(
        timestamp=datetime.datetime.now(),
        guild=g,
        member_count=0,
        online_count=0,
    )
    assert c

def test_channel_metrics_read():
    g = Guild.find(name="")
    c = ChannelMetrics.get_timeseries(guild=g, duration="1d")
    pprint(c)
    assert len(c) > 0
