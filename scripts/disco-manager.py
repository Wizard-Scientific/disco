#!/usr/bin/env python3

import os
import sys
import logging
import datetime

import click

import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from disco.models.utils.admin import dump_all, load_all, drop_db
from disco.models import Guild, ChannelMetrics
from disco.models.genesis import do_genesis


@click.group()
def cli():
    pass

@click.command()
def drop():
    drop_db()

@click.command()
def genesis():
    do_genesis()

@click.command()
def repl():
    import IPython
    IPython.embed()

@click.command()
@click.argument('path')
def dump(path):
    dump_all(path)

@click.command()
@click.argument('path')
def load(path):
    load_all(path)


cli.add_command(load)
cli.add_command(dump)
cli.add_command(repl)
cli.add_command(genesis)
cli.add_command(drop)


if __name__ == "__main__":
    cli()
