from ..guild import Guild


def do_genesis():
    Guild.create(name="Bot Dev")
