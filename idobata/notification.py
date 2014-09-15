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
from trac.util.text import exception_to_unicode
from trac.util.text import obfuscate_email_address

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
        id = ticket.id
        summary = ticket['summary']
        author = self.obfuscate_email(author)
        comment = self.wiki_to_html(id,comment)
        link = self.env.abs_href.ticket(id)
        status = ticket['status']
        message = u"""<a href='{link}'>#{id}&nbsp;:&nbsp;{summary}</a>&nbsp;<span class='label label-info'>{status}</span>&nbsp; by {author}
<p>
{comment}
</p>
"""
        message = message.format(id=id,summary=summary,link=link,comment=comment,author=author,status=status)
        self._do_post(message)
        return

    def _post_ticket_hook(self,event,event_class,ticket):
        id = ticket.id
        summary = ticket['summary']
        desc = ticket['description']
        reporter = ticket['reporter']
        reporter = self.obfuscate_email(reporter)
        desc = self.wiki_to_html(id, desc)
        link = self.env.abs_href.ticket(id)
        message = u"""<a href='{link}'>#{id}&nbsp;:&nbsp;{summary}</a>&nbsp;<span class='label label-{event_class}'>{event}</span> by {reporter}
<p>
{desc}
</p>
"""
        message = message.format(event=event,event_class=event_class,id=id,summary=summary,link=link,desc=desc,reporter=reporter)
        self._do_post(message)
        return

    def _do_post(self,message):
        params=urllib.urlencode({'source':message.encode('utf-8'),'format':'html'})
        urllib.urlopen(self.endpoint,params)
        return

    def wiki_to_html(self, id, wikitext):
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
            context = Context.from_request(req, 'ticket', id)
            formatter = HtmlFormatter(self.env, context, wikitext)
            return formatter.generate(True)
        except Exception, e:
            raise
            self.log.error("Failed to render %s", repr(wikitext))
            self.log.error(exception_to_unicode(e, traceback=True))
            return wikitext

    def obfuscate_email(self, text):
        if self.env.config.getbool('trac', 'show_email_addresses'):
            return text
        else:
            return obfuscate_email_address(text)

class WikiNotification(Component):
    implements(IWikiChangeListener)

    endpoint = Option('idobata','endpoint','https://idobata.io/hook/XXX',"""
idobata hook endpoint
""")
    wiki_detail = BoolOption('idobata','wiki_detail',True,"show wiki's detail information")

    def wiki_page_added(self,page):
        self._post_wiki_hook('CREATED',page)
        return

    def wiki_page_changed(self,page, version, t, comment, author, ipnr):
        self._post_wiki_hook('Update',page)
        return

    def wiki_page_deleted(self,page):
        self._post_wiki_hook('DELETE',page)
        return

    def wiki_page_version_deleted(self,page):
        self._post_wiki_hook('Delete version',page)
        return

    def wiki_page_renamed(self,page, old_name):
        name = page.name
        link = self.env.abs_href.wiki(name)
        message = u"""<a href='{link}'>wiki:{name}</a>&nbsp;<span class='label label-info'>RENAME</span> from {old_name}"""
        message = message.format(link=link,old_name=old_name,name=name)
        self._do_post(message)
        return

    def _post_wiki_hook(self,event,page):
        name = page.name
        link = self.env.abs_href.wiki(name)
        text = page.text
        
        if self.wiki_detail:
            text = page.text
            text = self.wiki_to_html(name,text)
            message = u"""<a href='{link}'>wiki:{name}</a>&nbsp;<span class='label label-success'>{event}</span>
<p>
{text}
</p>
"""
            message = message.format(event=event,link=link,name=name,text=text)
            self._do_post(message)
            return
        else:
            version = page.version
            old_version = version - 1
            message = "<a href='{link}?action=diff&version={version}&old_version={old_version}'>Wiki:{name} is changed. version:{version}</a>&nbsp;<span class='label label-success'>{event}</span>"
            message = message.format(event=event,link=link,name=name,version=version,old_version=old_version)
            self._do_post(message)
            return

    def _do_post(self,message):
        params=urllib.urlencode({'source':message.encode('utf-8'),'format':'html'})
        urllib.urlopen(self.endpoint,params)
        return

    def wiki_to_html(self, name, wikitext):
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
