# -*- coding: utf-8 -*-
"""
    flask.ext.fillin.wrapper
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Add modifiy response class with form parsing support.

    :copyright: (c) 2012 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

import types

from flask.wrappers import Response
from lxml.html import document_fromstring

class FormWrapper(Response):
    """An additional wrapper for the :class:`~flask.testing.FlaskClient` which
    adds :data:`form` and :data:`forms` as parameter of the response.::

        from flask.ext.fillin import FormWrapper

        client = FlaskClient(flask_app, response_wrapper=FormWrapper)
        response = client.get('/page_with_form')

        response.form.fields['username'] = 'my username'
        response.form.fields['password'] = 'secret'
        response.form.fields['remember'] = True

        response.form.submit(client)

        Adds also :data:`html` which is parsed lxml HtmlElement and methods
        :data:`link` and :data:`links` for link access.

        Each link has method click(client) which calls client.get(href).
    """

    _parsed_html = None


    @property
    def html(self):
        if self._parsed_html is None:
            self._parsed_html = document_fromstring(self.data)

            # add click function to all links
            def _click(self, client, **kwargs):
                path = self.attrib['href']
                return client.get(path, **kwargs)

            for link in self._parsed_html.cssselect('a'):
                setattr(link, 'click', types.MethodType(_click, link))

            # add submit function to all links
            def _submit(self, client, path=None, submit_name=None, **kargs):
                data = { k: '' if self._should_be_blank(k, v) else v
                               for k, v in self.fields.iteritems() }

                # validate and set values from files
                for key, value in self.files.iteritems():
                    if key not in self.inputs:
                        raise ValueError("No input of with name %s" % repr(key))
                    if self.inputs[key].type != "file":
                        raise ValueError("Input %s is not of type 'file'" % repr(key))
                    if not isinstance(value, file):
                        raise TypeError("Set file input %s with non-file %s" % (repr(key), repr(value)))
                    data[key] = value

                if kargs.has_key('data'):
                    data.update(kargs['data'])
                    del kargs['data']
                if path is None:
                    path = self.action
                if not kargs.has_key('method'):
                    kargs['method'] = self.method
                return client.open(path, data=data, **kargs)

            def _should_be_blank(self, k, v):
                # note that most browsers submit '' instead of None for empty fields
                blank_fields = ['text', 'password']

                field = self.inputs[k]
                if hasattr(field, 'type'):
                  return field.type in blank_fields and v is None
                else:
                  return False

            for form in self._parsed_html.forms:
                setattr(form, "files", {})  # TODO, validate that input is a file handle upon assigment
                setattr(form, "submit", types.MethodType(_submit, form))
                setattr(form, "_should_be_blank", types.MethodType(_should_be_blank, form))

        return self._parsed_html

    @property
    def forms(self):
        """A list of all received forms in the same way like
        `lxml <http://lxml.de/lxmlhtml.html#forms>`_ with the same functions
        and an additional function to submit the form over a test client.
        """
        return self.html.forms

    @property
    def form(self):
        """The first received form from the page."""
        return self.forms[0]

    def links(self, css_expression="a"):
        """Get all the links by css_express"""
        return self.html.cssselect(css_expression)

    def link(self, css_expression="a"):
        """Get first link by css_expression"""
        links = self.links(css_expression)
        if links:
            return links[0]
