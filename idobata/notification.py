# -*- coding: utf-8 -*-
from trac.core import *
from trac.ticket.model import Ticket
from trac.ticket.api import ITicketChangeListener
from trac.wiki.api import IWikiChangeListener
from trac.wiki.formatter import format_to_html
from trac.config import *
from trac.test import Mock,MockPerm
from trac.web.href import Href
from trac.mimeview import Context
from trac.wiki.formatter import HtmlFormatter

import urllib

class TicketNotification(Component):
    implements(ITicketChangeListener)

    endpoint = Option('idobata','endpoint','https://idobata.io/hook/XXX',"""
idobata hoook endpoint
""")

    def ticket_created(self,ticket):
        self._post_ticket_hook('CREATED','success',ticket)
        return

    def ticket_deleted(self,ticket):
        self._post_ticket_hook('DELETED','important',ticket)
        return

    def ticket_changed(self,ticket, comment, author, old_values):
        return

    def _post_ticket_hook(self,event,event_class,ticket):
        id = ticket.id
        summary = ticket['summary']
        desc = ticket['description']
        desc = self.wiki_to_html('ticket', ticket.id, desc)
        link = self.env.abs_href.ticket(ticket.id)
        message = u"""<span class='label label-{event_class}'>TICKET:{event}</span>&nbsp;<a href='{link}'>{id}:{summary}</a>
{desc}
"""
        message = message.format(event=event,event_class=event_class,id=id,summary=summary,link=link,desc=desc)
        self._do_post(message)
        return

    def _do_post(self,message):
        params=urllib.urlencode({'source':message.encode('utf-8'),'format':'html'})
	urllib.urlopen(self.endpoint,params)
        return

    def wiki_to_html(self, realm, id, wikitext):
        if wikitext is None:
            return ""
        try:
            req = Mock(
                href=Href(self.env.abs_href()),
                abs_href=self.env.abs_href,
                authname='',
                perm=MockPerm(),
                chrome=dict(
                    warnings=[],
                    notices=[]
                ),
                args={}
            )
            context = Context.from_request(req, realm, id)
            formatter = HtmlFormatter(self.env, context, wikitext)
            return formatter.generate(True)
        except Exception, e:
            raise
            self.log.error("Failed to render %s", repr(wikitext))
            self.log.error(exception_to_unicode(e, traceback=True))
            return wikitext

class WikiNotification(Component):
    implements(IWikiChangeListener)

    endpoint = Option('idobata','endpoint','https://idobata.io/hook/XXX',"""
idobata hoook endpoint
""")

    def wiki_page_added(self,page):
        self._post_wiki_hook('CREATED',page)
        return

    def wiki_page_changed(page, version, t, comment, author, ipnr):
        return

    def wiki_page_deleted(page):
        return

    def wiki_page_version_deleted(page):
        return

    def wiki_page_renamed(page, old_name):
        name = page.name
        link = self.env.abs_href.wiki(name)
        message = u"""<span class='label label-warn'>WIKI:RENAME</span>&nbsp;{old_name}-><a href='{link}'>{name}</a>"""
        message = message.format(event=event,link=link,old_name=old_name,name=name)
        self._do_post(message)
        return

    def _post_wiki_hook(self,event,page):
        name = page.name
        link = self.env.abs_href.wiki(name)
        text = page.text
        text = self.wiki_to_html(name,text)
        message = u"""<span class='label label-success'>WIKI:{event}</span>&nbsp;<a href='{link}'>{name}</a>
{text}
"""
        message = message.format(event=event,link=link,name=name,text=text)
        self._do_post(message)
        return

    def _do_post(self,message):
        params=urllib.urlencode({'source':message.encode('utf-8'),'format':'html'})
	urllib.urlopen(self.endpoint,params)
        return
    
    def wiki_to_html(self, name , wikitext):
        if wikitext is None:
            return ""
        try:
            req = Mock(
                href=Href(self.env.abs_href()),
                abs_href=self.env.abs_href,
                authname='',
                perm=MockPerm(),
                chrome=dict(
                    warnings=[],
                    notices=[]
                ),
                args={}
            )
            context = Context.from_request(req, 'wiki',name)
            formatter = HtmlFormatter(self.env, context, wikitext)
            return formatter.generate(True)
        except Exception, e:
            raise
            self.log.error("Failed to render %s", repr(wikitext))
            self.log.error(exception_to_unicode(e, traceback=True))
            return wikitext
