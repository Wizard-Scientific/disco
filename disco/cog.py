from discord.ext import commands

from .permissions import PermissionsHelper
from .utils.config import init_config
from .utils.logger import init_logger


class BaseCog(PermissionsHelper, commands.Cog):
    def __init__(self):
        self.config = init_config()
        self.logger = init_logger()
        super().__init__()
