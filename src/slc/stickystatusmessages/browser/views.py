from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from slc.stickystatusmessages.config import SSMKEY
from interfaces import IStickyStatusMessagesViewlet
from interfaces import IAJAXView
from slc.stickystatusmessages.interfaces import IStickyStatusMessagesSettings
from slc.stickystatusmessages import StickyStatusMessageFactory as _

class StickyStatusMessagesViewlet(ViewletBase):
    """ """
    implements(IStickyStatusMessagesViewlet)
    index = ViewPageTemplateFile('templates/stickystatusmessages.pt')

    def messages(self):
        """ """
        context = aq_inner(self.context)
        mtool = getToolByName(context, 'portal_membership')
        if mtool.isAnonymousUser():
            return []

        member = mtool.getAuthenticatedMember()
        annotations = IAnnotations(member)
        ssm = annotations.get(SSMKEY, {})
        return ssm.values()


class StickyStatusMessagesAJAXView(BrowserView):
    implements(IAJAXView)
    
    def delete_all_messages(self):
        """ Remove all the currently stored sticky messages by simply
            replacing the annotations with a new empty dict.
        """
        context = aq_inner(self.context)
        mtool = getToolByName(context, 'portal_membership')
        if mtool.isAnonymousUser():
            return

        member = mtool.getAuthenticatedMember()
        annotations = IAnnotations(member)
        annotations[SSMKEY] = {}


    def delete_message(self, message_id):
        """ """
        context = aq_inner(self.context)
        mtool = getToolByName(context, 'portal_membership')
        if mtool.isAnonymousUser():
            return []

        member = mtool.getAuthenticatedMember()
        annotations = IAnnotations(member)
        ssm = annotations.get(SSMKEY, {})
        if ssm.has_key(message_id):
            del ssm[message_id]
        annotations[SSMKEY] = ssm


class StickyStatusMessagesSettings(RegistryEditForm):
    schema = IStickyStatusMessagesSettings
    label = _(u"Sticky Status Message Settings")
    description = _(u"Use the settings below to configure "
                    u"slc.stickystatusmessages for this site")

class StickyStatusMessagesControlPanel(ControlPanelFormWrapper):
    form = StickyStatusMessagesSettings

