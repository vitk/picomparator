# -*- coding: utf-8 -*-
import wx
from docpage import DocPage
from settings import FILENAME_FONT, COMMENT_FONT


class DocListBox(wx.VListBox):
    def __init__(self, parent, docs):
        super(DocListBox, self).__init__(parent)
        self.docs = docs
        """
        @type : Document
        """
        self.SetItemCount(len(docs))

        self.labelFont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.labelFont.SetPointSize(10)
        self.labelFont.SetFaceName(FILENAME_FONT)

        self.commentFont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.commentFont.SetPointSize(9)
        self.commentFont.SetFaceName(COMMENT_FONT)

    def OnMeasureItem(self, index):
        return 35

    def OnDrawSeparator(self, dc, rect, index):
        oldpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.DrawLine(rect.x, rect.y, rect.x + rect.width, rect.y)

        dc.SetPen(oldpen)

    def OnDrawItem(self, dc, rect, index):
        '''
        :type dc: wx.DC
        :type rect: wx.Rect
        :type index: int
        '''
        doc = self.docs[index]
        """ @type: Document"""


        if doc.hasStatus():
            dc.SetPen(wx.TRANSPARENT_PEN)
            brushColour = wx.Colour(155, 155, 155)
            if doc.status == "progress":
                brushColour = wx.Colour(50, 200, 50)
            elif doc.status == "regress":
                brushColour = wx.Colour(200, 50, 50)
            dc.SetBrush(wx.Brush(brushColour))
            dc.DrawRectangle(rect.x + 1, rect.y + 2, 5, rect.height - 3)

        labelRect = wx.Rect(rect.x + 15, rect.y + 2, rect.width - 20, rect.height / 2 - 4)
        commentRect = wx.Rect(labelRect.x, labelRect.y + labelRect.height + 2, labelRect.width, labelRect.height)

        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetFont(self.labelFont)
        dc.SetTextForeground(wx.BLACK if doc.isCompared() else wx.Colour(135, 135, 135))
        dc.DrawLabel(doc.key, labelRect)
        dc.SetFont(self.commentFont)
        if not doc.hasComment():
            dc.SetTextForeground(wx.RED)
            dc.DrawLabel("not commented", commentRect)
        else:
            dc.SetTextForeground(wx.BLUE)
            dc.DrawLabel(doc.comment, commentRect)

    def GetItem(self, index):
        return self.docs[index]

