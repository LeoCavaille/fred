#!/usr/bin/env python

from fred.orm import Changes
from fred.daemon import Session

import logging
import fedmsg
import fedmsg.consumers

import datetime as dt

class ArchiveLurker(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.debian.dev.debmessenger.package.upload'
    config_key = 'fred'

    def __init__(self, *args, **kwargs):
        super(ArchiveLurker, self).__init__(*args, **kwargs)

    def consume(self, message):
        # We do not need to validate the changes, as it is an automatic message 
        # from the archive
        session = Session()
        m = message['body']['msg']
        logging.info("Received a fedmsg about changes, package : %s/%s", m["Source"], m["Version"])
        c = Changes(
                nameversion = "%s/%s" % (m["Source"], m["Version"]),
                name = m["Source"],
                version = m["Version"],
                suite = m["Distribution"],
                created_at = dt.datetime.utcnow())
        session.add(c)
        session.commit()
