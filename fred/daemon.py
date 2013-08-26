#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ricky.utils import fetch_and_upload
import ricky

import subprocess
import os
import logging
import time
from threading import Thread

from fred.orm import Changes
from fedmsg.commands.hub import hub
# TODO CONFIG
#from fred.config import Config

#conf = Config()

# TODO CONFIG
MIRROR = 'ftp.fr.debian.org'

# TODO CONFIG
engine = create_engine('sqlite:///buildbuffer.db', echo=True)
Session = sessionmaker(bind=engine)

def main_loop():
    session = Session()
    while True:
        time.sleep(60)
        for mirror in ["incoming.debian.org", MIRROR]:
            ricky.DEFAULT_MIRROR = mirror
            pending = session.query(Changes).all()
            for c in pending:
                try:
                    logging.debug("Trying to upload with ricky %s for auto-rebuild", c.nameversion)
                    fetch_and_upload(
                        source=c.name,
                        version=c.version,
                        dist=c.suite,
                        **{"X-Debile-Group": "auto-rebuild"}
                    )
                    logging.info("Uploaded %s", c.nameversion)
                    session.delete(c)
                    session.commit()
                except Exception as e:
                    logging.warn("OOPS could not upload (%s), I will be retrying however", e)

def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)8s - [fred] %(message)s', level=logging.DEBUG)
    logging.info("Booting fred daemon")
    if not os.path.exists('/etc/fedmsg.d/fred.py'):
        logging.error("Please copy the fred fedmsg config (config_fred.py) to /etc/fedmsg.d/fred.py")
        return 1

    # Fork to launch fedmsg-hub
    t = Thread(target=main_loop)
    t.setDaemon(True)
    t.start()

    hub()


if __name__ == "__main__":
    main()
