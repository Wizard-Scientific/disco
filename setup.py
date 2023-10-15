from setuptools import setup, find_packages
import os
import re


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


file_text = read(fpath('disco/__meta__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    version=grep('__version__'),
    name='disco',
    description="Disco",
    packages=["disco"],
    scripts=[
        "scripts/disco-manager.py",
        "scripts/basic-disco-bot.py",
    ],
    include_package_data=True,
    keywords='',
    author=grep('__author__'),
    author_email=grep('__email__'),
    url=grep('__url__'),
    install_requires=[
        'discord.py==1.7.3',
        'SQLAlchemy==1.4.42',
        'click==8.1.3',
        'pytest',
        'requests',
        'python-dotenv',
        'psycopg2-binary',
        'alembic',
        'pycoingecko',
        'pandas',
        'seaborn',
        'ipython',
        'wheel',
    ],
    license='MIT',
    zip_safe=False,
)
