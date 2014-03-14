# -*- coding: utf-8 -*-
from trac.core import *
from trac.ticket.model import Ticket
from trac.ticket.api import ITicketChangeListener
from trac.config import *
from trac.util.text import obfuscate_email_address

import urllib
import md5


class IdobataNotificationPlugin(Component):
    implements(ITicketChangeListener)

    endpoint = Option('idobata','endpoint','https://idobata.io/hook/XXX',"""
idobata hoook endpoint
""")

    # ITicketChangeListener methods
    def ticket_created(self,ticket):
        self.env.log.debug('ticket created')
        self._post_hook('CREATED',ticket,ticket['reporter'])
        return

    def ticket_deleted(self,ticket):
        self.env.log.debug('ticket deleted')
        self._post_hook('DELETED',ticket,ticket['reporter'])
        return

    def ticket_changed(self,ticket, comment, author, old_values):
        self.env.log.debug('ticket changed')
        self._post_hook(ticket['status'],ticket,author)
        return

    def _post_hook(self,event,ticket,author):
        id = ticket.id
        summary = ticket['summary']
        link = self.env.abs_href.ticket(ticket.id)
        author = self.obfuscate_email(author)
        message = u"[{event}]<a href="{link}">{id}:{summary}</a><br/>".format(event=event,author=author,id=id,summary=summary,link=link)
        params=urllib.urlencode({'source':message.encode('utf-8')})
	      urllib.urlopen(url,params)
