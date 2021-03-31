from math import ceil, floor, sqrt

import wx
from PIL import Image
from svgelements import (Arc, Close, Color, CubicBezier, Group, Line, Matrix,
                         Move, Path, QuadraticBezier, Shape, SVGImage, SVGText)

from .zmatrix import ZMatrix
from ..core.cutcode import LineCut, QuadCut, CubicCut, CutCode, RasterCut

"""
Laser Render provides GUI relevant methods of displaying the given project.
"""


DRAW_MODE_GUIDES = 0x000002
DRAW_MODE_GRID = 0x000004
DRAW_MODE_ESTIMATE = 0x000001
DRAW_MODE_CUT = 0x000008
DRAW_MODE_ENGRAVE = 0x000010
DRAW_MODE_RASTER = 0x000020
DRAW_MODE_GCODE = 0x000040

DRAW_MODE_ZOOM = 0x000080
DRAW_MODE_REFRESH = 0x000100
DRAW_MODE_ANIMATE = 0x000200
DRAW_MODE_PATH = 0x000400
DRAW_MODE_IMAGE = 0x000800
DRAW_MODE_TEXT = 0x001000
DRAW_MODE_BACKGROUND = 0x002000
DRAW_MODE_ICONS = 0x0040000
DRAW_MODE_TREE = 0x0080000
DRAW_MODE_INVERT = 0x400000
DRAW_MODE_FLIPXY = 0x800000


def swizzlecolor(c):
    if c is None:
        return None
    if isinstance(c, int):
        c = Color(c)
    if c.value is None:
        return None
    return c.blue << 16 | c.green << 8 | c.red


class LaserRender:
    def __init__(self, context):
        self.context = context
        self.pen = wx.Pen()
        self.brush = wx.Brush()
        self.color = wx.Colour()

    def render_cut(self, cutcode: CutCode, gc: wx.GraphicsContext):
        """
        Render scene information.
        """
        if not len(cutcode):
            return
        p = gc.CreatePath()
        last_point = None
        gc.SetPen(wx.RED_PEN)
        for cut in cutcode:
            start = cut.start()
            end = cut.end()
            if last_point != start:
                p.MoveToPoint(start[0], start[1])
            if isinstance(cut, LineCut):
                p.AddLineToPoint(end[0], end[1])
            elif isinstance(cut, QuadCut):
                p.AddQuadCurveToPoint(cut.control[0], cut.control[1], end[0], end[1])
            elif isinstance(cut, CubicCut):
                p.AddCurveToPoint(
                    cut.control1[0],
                    cut.control1[1],
                    cut.control2[0],
                    cut.control2[1],
                    end[0],
                    end[1],
                )
            elif isinstance(cut, RasterCut):
                image = cut.image
                try:
                    matrix = image.transform
                except AttributeError:
                    matrix = Matrix()
                gc.PushState()
                gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
                cache = None
                try:
                    cache = cut.cache
                except AttributeError:
                    pass
                if cache is None:
                    max_allowed = 2048
                    cut.c_width, cut.c_height = image.image.size
                    cut.cache = self.make_thumbnail(image.image, maximum=max_allowed)
                gc.DrawBitmap(cut.cache, 0, 0, cut.c_width, cut.c_height)
                gc.PopState()
            last_point = end
        gc.StrokePath(p)
        del p

    def render_engrave(self, cutcode: CutCode, gc: wx.GraphicsContext):
        """
        Render scene information.
        """
        if not len(cutcode):
            return
        p = gc.CreatePath()
        last_point = None
        gc.SetPen(wx.BLUE_PEN)
        for cut in cutcode:
            start = cut.start()
            end = cut.end()
            if last_point != start:
                p.MoveToPoint(start[0], start[1])
            if isinstance(cut, LineCut):
                p.AddLineToPoint(end[0], end[1])
            elif isinstance(cut, QuadCut):
                p.AddQuadCurveToPoint(cut.control[0], cut.control[1], end[0], end[1])
            elif isinstance(cut, CubicCut):
                p.AddCurveToPoint(
                    cut.control1[0],
                    cut.control1[1],
                    cut.control2[0],
                    cut.control2[1],
                    end[0],
                    end[1],
                )
            elif isinstance(cut, RasterCut):
                image = cut.image
                try:
                    matrix = image.transform
                except AttributeError:
                    matrix = Matrix()
                gc.PushState()
                gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
                cache = None
                try:
                    cache = cut.cache
                except AttributeError:
                    pass
                if cache is None:
                    max_allowed = 2048
                    cut.c_width, cut.c_height = image.image.size
                    cut.cache = self.make_thumbnail(image.image, maximum=max_allowed)
                gc.DrawBitmap(cut.cache, 0, 0, cut.c_width, cut.c_height)
                gc.PopState()
            last_point = end
        gc.StrokePath(p)
        del p

    def render_raster(self, cutcode: CutCode, gc: wx.GraphicsContext):
        """
        Render scene information.
        """
        if not len(cutcode):
            return
        p = gc.CreatePath()
        last_point = None
        gc.SetPen(wx.BLACK_PEN)
        for cut in cutcode:
            start = cut.start()
            end = cut.end()
            if last_point != start:
                p.MoveToPoint(start[0], start[1])
            if isinstance(cut, LineCut):
                p.AddLineToPoint(end[0], end[1])
            elif isinstance(cut, QuadCut):
                p.AddQuadCurveToPoint(cut.control[0], cut.control[1], end[0], end[1])
            elif isinstance(cut, CubicCut):
                p.AddCurveToPoint(
                    cut.control1[0],
                    cut.control1[1],
                    cut.control2[0],
                    cut.control2[1],
                    end[0],
                    end[1],
                )
            elif isinstance(cut, RasterCut):
                image = cut.image
                try:
                    matrix = image.transform
                except AttributeError:
                    matrix = Matrix()
                gc.PushState()
                gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
                cache = None
                try:
                    cache = cut.cache
                except AttributeError:
                    pass
                if cache is None:
                    max_allowed = 2048
                    cut.c_width, cut.c_height = image.image.size
                    cut.cache = self.make_thumbnail(image.image, maximum=max_allowed)
                gc.DrawBitmap(cut.cache, 0, 0, cut.c_width, cut.c_height)
                gc.PopState()
            last_point = end
        gc.StrokePath(p)
        del p

    def render_gcode(self, cutcode: CutCode, gc: wx.GraphicsContext):
        """
        Render scene information.
        """
        if not len(cutcode):
            return
        p = gc.CreatePath()
        last_point = None
        self.pen.SetColour(wx.GREEN_PEN)
        gc.SetPen(self.pen)
        for cut in cutcode:
            start = cut.start()
            end = cut.end()
            if last_point != start:
                p.MoveToPoint(start[0], start[1])
            if isinstance(cut, LineCut):
                p.AddLineToPoint(end[0], end[1])
            elif isinstance(cut, QuadCut):
                p.AddQuadCurveToPoint(cut.control[0], cut.control[1], end[0], end[1])
            elif isinstance(cut, CubicCut):
                p.AddCurveToPoint(
                    cut.control1[0],
                    cut.control1[1],
                    cut.control2[0],
                    cut.control2[1],
                    end[0],
                    end[1],
                )
            elif isinstance(cut, RasterCut):
                image = cut.image
                try:
                    matrix = image.transform
                except AttributeError:
                    matrix = Matrix()
                gc.PushState()
                gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
                cache = None
                try:
                    cache = cut.cache
                except AttributeError:
                    pass
                if cache is None:
                    max_allowed = 2048
                    cut.c_width, cut.c_height = image.image.size
                    cut.cache = self.make_thumbnail(image.image, maximum=max_allowed)
                gc.DrawBitmap(cut.cache, 0, 0, cut.c_width, cut.c_height)
                gc.PopState()
            last_point = end
        gc.StrokePath(p)
        del p

    def set_pen(self, gc, stroke, width=1.0):
        c = stroke
        if c is not None and c != "none":
            swizzle_color = swizzlecolor(c)
            self.color.SetRGBA(swizzle_color | c.alpha << 24)  # wx has BBGGRR
            self.pen.SetColour(self.color)
            self.pen.SetWidth(width)
            gc.SetPen(self.pen)
        else:
            gc.SetPen(wx.TRANSPARENT_PEN)

    def set_brush(self, gc, fill):
        c = fill
        if c is not None and c != "none":
            swizzle_color = swizzlecolor(c)
            self.color.SetRGBA(swizzle_color | c.alpha << 24)  # wx has BBGGRR
            self.brush.SetColour(self.color)
            gc.SetBrush(self.brush)
        else:
            gc.SetBrush(wx.TRANSPARENT_BRUSH)

    def set_element_pen(self, gc, element, zoomscale=1.0, width_scale=None):
        try:
            sw = element.stroke_width
        except AttributeError:
            sw = 1.0
        if sw is None:
            sw = 1.0
        limit = zoomscale ** 0.5
        limit /= width_scale
        if sw < limit:
            sw = limit
        self.set_pen(gc, element.stroke, width=sw)

    def set_element_brush(self, gc, element):
        self.set_brush(gc, element.fill)

    def make_thumbnail(self, pil_data, maximum=None, width=None, height=None):
        """Resizes the given pil image into wx.Bitmap object that fits the constraints."""
        image_width, image_height = pil_data.size
        if width is not None and height is None:
            height = width * image_height / float(image_width)
        if width is None and height is not None:
            width = height * image_width / float(image_height)
        if width is None and height is None:
            width = image_width
            height = image_height
        if maximum is not None and (width > maximum or height > maximum):
            scale_x = maximum / width
            scale_y = maximum / height
            scale = min(scale_x, scale_y)
            width = int(round(width * scale))
            height = int(round(height * scale))
        if image_width != width or image_height != height:
            pil_data = pil_data.copy().resize((width, height))
        else:
            pil_data = pil_data.copy()
        if pil_data.mode != "RGBA":
            pil_data = pil_data.convert("RGBA")
        pil_bytes = pil_data.tobytes()
        return wx.Bitmap.FromBufferRGBA(width, height, pil_bytes)
