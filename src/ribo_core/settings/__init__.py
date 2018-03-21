
from os.path import exists

#-# Use 12factor inspired environment variables or from a file
import environ
from os.path import dirname, join
import logging
import os
import re
import sys
import warnings
from six import string_types

logger = logging.getLogger(__name__)


class RiboEnv(environ.Env):

    @classmethod
    def read_env(cls, env_file=None, **overrides):
        """Read a .env file into os.environ.

        If not given a path to a dotenv path, does filthy magic stack backtracking
        to find manage.py and then find the dotenv.

        http://www.wellfireinteractive.com/blog/easier-12-factor-django/

        https://gist.github.com/bennylope/2999704
        """
        if env_file is None:
            frame = sys._getframe()
            env_file = os.path.join(os.path.dirname(frame.f_back.f_code.co_filename), '.env')
            if not os.path.exists(env_file):
                warnings.warn(
                    "%s doesn't exist - if you're not configuring your "
                    "environment separately, create one." % env_file)
                return

        try:
            with open(env_file, encoding='utf-8') if isinstance(env_file, string_types) else env_file as f:
                content = f.read()
        except IOError:
            warnings.warn(
                "Error reading %s - if you're not configuring your "
                "environment separately, check this." % env_file)
            return

        logger.debug('Read environment variables from: {0}'.format(env_file))

        for line in content.splitlines():
            m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
            if m1:
                key, val = m1.group(1), m1.group(2)
                m2 = re.match(r"\A'(.*)'\Z", val)
                if m2:
                    val = m2.group(1)
                m3 = re.match(r'\A"(.*)"\Z', val)
                if m3:
                    val = re.sub(r'\\(.)', r'\1', m3.group(1))
                cls.ENVIRON.setdefault(key, str(val))

        # set defaults
        for key, value in overrides.items():
            cls.ENVIRON.setdefault(key, value)

env = RiboEnv()

# Build paths inside the project like this: join(BASE_DIR, "directory")
BASE_DIR = dirname(dirname(dirname(__file__)))
# Ideally move env file should be outside the git repo
# i.e. BASE_DIR.parent.parent
env_file = join(dirname(BASE_DIR), "config.env")
if not exists(env_file):
    env_file = "/etc/ribo_core/config.env"
    
if exists(env_file):
    RiboEnv.read_env(str(env_file))