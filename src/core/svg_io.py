import os

from ..svgelements import SVG, Group, Path, Shape, SVGImage, SVGText

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
        bed_dim = context.get_context("bed")
        bed_dim.setting(float, "bed_width", 325.0)
        bed_dim.setting(float, "bed_height", 220.0)
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
        return SVGLoader.parse(svg, elements_modifier, pathname)

    @staticmethod
    def parse(svg, elements_modifier, pathname):
        for element in svg:
            try:
                if element.values["visibility"] == "hidden":
                    continue
            except KeyError:
                pass
            except AttributeError:
                pass
            # if isinstance(element, SVGText):
            #     if element.text is None:
            #         continue
            #     if element.stroke == "red":
            #         elements_modifier.cut_cutcode(element)
            #     elif element.stroke == "blue":
            #         elements_modifier.engrave_cutcode(element)
            #     else:
            #         elements_modifier.raster_cutcode(element)
            if isinstance(element, Path):
                if len(element) == 0:
                    continue
                element.approximate_arcs_with_cubics()
                if element.stroke == "red":
                    elements_modifier.cut_cutcode(abs(element))
                elif element.stroke == "blue":
                    elements_modifier.engrave_cutcode(abs(element))
                else:
                    elements_modifier.raster_cutcode(abs(element))
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
                if element.stroke == "red":
                    elements_modifier.cut_cutcode(abs(Path(element)))
                elif element.stroke == "blue":
                    elements_modifier.engrave_cutcode(abs(Path(element)))
                else:
                    elements_modifier.raster_cutcode(abs(Path(element)))
            # elif isinstance(element, SVGImage):
            #     try:
            #         element.load(os.path.dirname(pathname))
            #         if element.image is not None:
            #             elements_modifier.raster_cutcode(abs(element))
            #     except OSError:
            #         pass
            elif isinstance(element, SVG):
                continue
            elif isinstance(element, Group):
                SVGLoader.parse(element, elements_modifier, pathname)
                continue
        return True
