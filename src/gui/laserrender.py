from math import ceil, floor, sqrt

import wx
from PIL import Image
from svgelements import (Arc, Close, Color, CubicBezier, Group, Line, Matrix,
                         Move, Path, QuadraticBezier, Shape, SVGImage, SVGText)

from .zmatrix import ZMatrix
from ..core.cutcode import LineCut, QuadCut, CubicCut, CutCode

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

    def draw_group_node(self, node, gc, draw_mode, zoomscale=1.0):
        pass

    def draw_shape_node(self, node, gc, draw_mode, zoomscale=1.0):
        """Default draw routine for the shape element."""
        shape = node.object
        try:
            matrix = shape.transform
            width_scale = sqrt(abs(matrix.determinant))
        except AttributeError:
            matrix = Matrix()
            width_scale = 1.0
        if not hasattr(node, "cache") or node.cache is None:
            cache = self.make_path(gc, Path(shape))
            node.cache = cache
        gc.PushState()
        gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
        self.set_element_pen(gc, shape, zoomscale=zoomscale, width_scale=width_scale)
        self.set_element_brush(gc, shape)
        # if draw_mode & DRAW_MODE_FILLS == 0 and shape.fill is not None:
        #     gc.FillPath(node.cache)
        # if draw_mode & DRAW_MODE_STROKES == 0 and shape.stroke is not None:
        #     gc.StrokePath(node.cache)
        gc.PopState()

    def draw_path_node(self, node, gc, draw_mode, zoomscale=1.0):
        """Default draw routine for the laser path element."""
        path = node.object
        try:
            matrix = path.transform
            width_scale = sqrt(abs(matrix.determinant))
        except AttributeError:
            matrix = Matrix()
            width_scale = 1.0
        if not hasattr(node, "cache") or node.cache is None:
            cache = self.make_path(gc, path)
            node.cache = cache
        gc.PushState()
        gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
        self.set_element_pen(gc, path, zoomscale=zoomscale, width_scale=width_scale)
        self.set_element_brush(gc, path)
        if draw_mode & DRAW_MODE_FILLS == 0 and path.fill is not None:
            gc.FillPath(node.cache)
        if draw_mode & DRAW_MODE_GCODE == 0 and path.stroke is not None:
            gc.StrokePath(node.cache)
        gc.PopState()

    def draw_text_node(self, node, gc, draw_mode, zoomscale=1.0):
        text = node.object
        try:
            matrix = text.transform
            width_scale = sqrt(abs(matrix.determinant))
        except AttributeError:
            matrix = Matrix()
            width_scale = 1.0
        if hasattr(node, "wxfont"):
            font = node.wxfont
        else:
            if text.font_size < 1:
                if text.font_size > 0:
                    text.transform.pre_scale(
                        text.font_size, text.font_size, text.x, text.y
                    )
                text.font_size = 1  # No zero sized fonts.
            font = wx.Font(text.font_size, wx.SWISS, wx.NORMAL, wx.BOLD)
            try:
                f = []
                if text.font_family is not None:
                    f.append(str(text.font_family))
                if text.font_face is not None:
                    f.append(str(text.font_face))
                if text.font_weight is not None:
                    f.append(str(text.font_weight))
                f.append("%d" % text.font_size)
                font.SetNativeFontInfoUserDesc(" ".join(f))
            except Exception:
                pass
            node.wxfont = font

        gc.PushState()
        gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
        self.set_element_pen(gc, text, zoomscale=zoomscale, width_scale=width_scale)
        self.set_element_brush(gc, text)

        if text.fill is None or text.fill == "none":
            gc.SetFont(font, wx.BLACK)
        else:
            gc.SetFont(font, wx.Colour(swizzlecolor(text.fill)))

        x = text.x
        y = text.y
        if text.text is not None:
            text.width, text.height = gc.GetTextExtent(text.text)
            if not hasattr(text, "anchor") or text.anchor == "start":
                y -= text.height
            elif text.anchor == "middle":
                x -= text.width / 2
                y -= text.height
            elif text.anchor == "end":
                x -= text.width
                y -= text.height
            gc.DrawText(text.text, x, y)
        gc.PopState()

    def draw_image_node(self, node, gc, draw_mode, zoomscale=1.0):
        image = node.object
        try:
            matrix = image.transform
        except AttributeError:
            matrix = Matrix()
        gc.PushState()
        gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
        if draw_mode & DRAW_MODE_ZOOM == 0:
            cache = None
            try:
                cache = node.cache
            except AttributeError:
                pass
            if cache is None:
                try:
                    max_allowed = node.max_allowed
                except AttributeError:
                    max_allowed = 2048
                node.c_width, node.c_height = image.image.size
                node.cache = self.make_thumbnail(image.image, maximum=max_allowed)
            gc.DrawBitmap(node.cache, 0, 0, node.c_width, node.c_height)
        else:
            node.c_width, node.c_height = image.image.size
            cache = self.make_thumbnail(image.image)
            gc.DrawBitmap(cache, 0, 0, node.c_width, node.c_height)
        gc.PopState()

    def make_raster(
        self, elements, bounds, width=None, height=None, bitmap=False, step=1
    ):
        """
        Make Raster turns an iterable of elements and a bounds into an image of the designated size, taking into account
        the step size etc.

        This function requires both wxPython and Pillow.

        :param elements: elements to render.
        :param bounds: bounds of those elements for the viewport.
        :param width: desired width of the resulting raster
        :param height: desired height of the resulting raster
        :param bitmap: bitmap to use rather than provisioning
        :param step: raster step rate, int scale rate of the image.
        :return:
        """
        if bounds is None:
            return None
        xmin, ymin, xmax, ymax = bounds
        xmax = ceil(xmax)
        ymax = ceil(ymax)
        xmin = floor(xmin)
        ymin = floor(ymin)

        image_width = int(xmax - xmin)
        if image_width == 0:
            image_width = 1

        image_height = int(ymax - ymin)
        if image_height == 0:
            image_height = 1

        if width is None:
            width = image_width
        if height is None:
            height = image_height
        width /= float(step)
        height /= float(step)
        width = int(width)
        height = int(height)
        bmp = wx.Bitmap(width, height, 32)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()

        matrix = Matrix()
        matrix.post_translate(-xmin, -ymin)
        scale_x = width / float(image_width)
        scale_y = height / float(image_height)
        scale = min(scale_x, scale_y)
        matrix.post_scale(scale)

        gc = wx.GraphicsContext.Create(dc)
        gc.SetInterpolationQuality(wx.INTERPOLATION_BEST)
        gc.PushState()
        gc.ConcatTransform(wx.GraphicsContext.CreateMatrix(gc, ZMatrix(matrix)))
        if not isinstance(elements, (list, tuple)):
            elements = [elements]
        gc.SetBrush(wx.WHITE_BRUSH)
        gc.DrawRectangle(xmin - 1, ymin - 1, xmax + 1, ymax + 1)
        self.render(elements, gc)
        img = bmp.ConvertToImage()
        buf = img.GetData()
        image = Image.frombuffer(
            "RGB", tuple(bmp.GetSize()), bytes(buf), "raw", "RGB", 0, 1
        )
        gc.PopState()
        gc.Destroy()
        del dc
        if bitmap:
            return bmp
        return image

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
