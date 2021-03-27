import os

from svgelements import (SVG,  SVG_ATTR_TAG, SVG_TAG_TEXT, Color, Group, Path, Shape, SVGElement, SVGImage, SVGText)

MILS_PER_MM = 39.3701


def plugin(kernel, lifecycle=None):
    if lifecycle == "register":
        kernel.register("load/SVGLoader", SVGLoader)


class SVGLoader:
    @staticmethod
    def load_types():
        yield "Scalable Vector Graphics", ("svg",), "image/svg+xml"

    @staticmethod
    def load(context, elements_modifier, pathname, **kwargs):
        bed_dim = context.get_context("/")
        bed_dim.setting(int, "bed_width", 310)
        bed_dim.setting(int, "bed_height", 210)
        if "svg_ppi" in kwargs:
            ppi = float(kwargs["svg_ppi"])
        else:
            ppi = 96.0
        if ppi == 0:
            ppi = 96.0
        scale_factor = 1000.0 / ppi
        svg = SVG.parse(
            source=pathname,
            reify=False,
            width="%fmm" % (bed_dim.bed_width),
            height="%fmm" % (bed_dim.bed_height),
            ppi=ppi,
            color="none",
            transform="scale(%f)" % scale_factor,
        )
        context_node = elements_modifier.get(type="branch elems")
        basename = os.path.basename(pathname)
        file_node = context_node.add(type="file", name=basename)
        file_node.filepath = pathname
        return SVGLoader.parse(
            svg, elements_modifier, file_node, pathname, scale_factor
        )

    @staticmethod
    def parse(svg, elements_modifier, context_node, pathname, scale_factor):
        for element in svg:
            try:
                if element.values["visibility"] == "hidden":
                    continue
            except KeyError:
                pass
            except AttributeError:
                pass
            if isinstance(element, SVGText):
                if element.text is None:
                    continue
                context_node.add(element, type="elem")
                elements_modifier.classify([element])
            elif isinstance(element, Path):
                if len(element) == 0:
                    continue
                element.approximate_arcs_with_cubics()
                context_node.add(element, type="elem")
                elements_modifier.classify([element])
            elif isinstance(element, Shape):
                if not element.transform.is_identity():
                    # Shape Reification failed.
                    element = Path(element)
                    element.reify()
                    element.approximate_arcs_with_cubics()
                    if len(element) == 0:
                        continue  # Degenerate.
                else:
                    e = Path(element)
                    if len(e) == 0:
                        continue  # Degenerate.
                context_node.add(element, type="elem")
                elements_modifier.classify([element])
            elif isinstance(element, SVGImage):
                try:
                    element.load(os.path.dirname(pathname))
                    if element.image is not None:
                        context_node.add(element, type="elem")
                        elements_modifier.classify([element])
                except OSError:
                    pass
            elif isinstance(element, SVG):
                continue
            elif isinstance(element, Group):
                new_context = context_node.add(type="group", name=element.id)
                SVGLoader.parse(element, elements_modifier, new_context, pathname, scale_factor)
                continue
        return True
