from svgelements import Color, SVGImage, SVGText

from ..kernel import Modifier
from .cutcode import CutCode, LaserSettings


def plugin(kernel, lifecycle=None):
    if lifecycle == "register":
        kernel.register("modifier/Elemental", ElementCore)
    elif lifecycle == "boot":
        kernel_root = kernel.get_context("/")
        kernel_root.activate("modifier/Elemental")


class ElementCore(Modifier):
    def __init__(self, context, name=None, channel=None, *args, **kwargs):
        Modifier.__init__(self, context, name, channel)
        self.engrave = CutCode()
        self.engrave_settings = LaserSettings(
            operation="Engrave", color="blue", speed=35.0
        )
        self.cut = CutCode()
        self.cut_settings = LaserSettings(operation="Cut", color="red", speed=10.0)
        self.raster = CutCode()
        self.raster_settings = LaserSettings(
            operation="Raster", color="black", speed=140.0
        )

    def attach(self, *a, **kwargs):
        context = self.context
        context.elements = self
        context.classify = self.classify
        context.save = self.save
        context.save_types = self.save_types
        context.load = self.load
        context.load_types = self.load_types

    def detach(self, *a, **kwargs):
        context = self.context
        settings = context.derive("operations")
        settings.clear_persistent()

        for i, op in enumerate(self.ops()):
            op_set = settings.derive(str(i))
            if not hasattr(op, "settings"):
                continue  # Might be a function.
            sets = op.settings
            for q in (op, sets):
                for key in dir(q):
                    if key.startswith("_"):
                        continue
                    if key.startswith("implicit"):
                        continue
                    value = getattr(q, key)
                    if value is None:
                        continue
                    if isinstance(value, Color):
                        value = value.value
                    op_set.write_persistent(key, value)
        settings.close_subpaths()

    def boot(self, *a, **kwargs):
        settings = self.context.derive("operations")
        subitems = list(settings.derivable())
        ops = [None] * len(subitems)
        for i, v in enumerate(subitems):
            op_setting_context = settings.derive(v)
            op = LaserOperation()
            op_set = op.settings
            op_setting_context.load_persistent_object(op)
            op_setting_context.load_persistent_object(op_set)
            try:
                ops[i] = op
            except (ValueError, IndexError):
                ops.append(op)
        if not len(ops) and self.context.operation_default_empty:
            self.load_default()
            return
        self.add_ops([o for o in ops if o is not None])

    @property
    def op_branch(self):
        return self._tree.get(type="branch ops")

    @property
    def elem_branch(self):
        return self._tree.get(type="branch elems")

    def ops(self, **kwargs):
        operations = self._tree.get(type="branch ops")
        for item in operations.flat(types=("op",), depth=1, **kwargs):
            yield item

    def elems(self, **kwargs):
        elements = self._tree.get(type="branch elems")
        for item in elements.flat(types=("elem",), **kwargs):
            yield item.object

    def elems_nodes(self, depth=None, **kwargs):
        elements = self._tree.get(type="branch elems")
        for item in elements.flat(
            types=("elem", "file", "group"), depth=depth, **kwargs
        ):
            yield item

    def first_element(self, **kwargs):
        for e in self.elems(**kwargs):
            return e
        return None

    def has_emphasis(self):
        for e in self.elems_nodes(emphasized=True):
            return True
        return False

    def count_elems(self, **kwargs):
        return len(list(self.elems(**kwargs)))

    def count_op(self, **kwargs):
        return len(list(self.ops(**kwargs)))

    def get(self, obj=None, type=None):
        return self._tree.get(obj=obj, type=type)

    def get_op(self, index, **kwargs):
        for i, op in enumerate(self.ops(**kwargs)):
            if i == index:
                return op
        raise IndexError

    def get_elem(self, index, **kwargs):
        for i, elem in enumerate(self.elems(**kwargs)):
            if i == index:
                return elem
        raise IndexError

    def get_elem_node(self, index, **kwargs):
        for i, elem in enumerate(self.elems(**kwargs)):
            if i == index:
                return elem
        raise IndexError

    def add_op(self, op):
        operation_branch = self._tree.get(type="branch ops")
        op.set_name(str(op))
        operation_branch.add(op, type="op")

    def add_ops(self, adding_ops):
        operation_branch = self._tree.get(type="branch ops")
        items = []
        for op in adding_ops:
            op.set_name(str(op))
            operation_branch.add(op, type="op")
            items.append(op)
        return items

    def add_elem(self, element):
        """
        Add an element. Wraps it within a node, and appends it to the tree.

        :param element:
        :return:
        """
        element_branch = self._tree.get(type="branch elems")
        node = element_branch.add(element, type="elem")
        self.context.signal("element_added", element)
        return node

    def add_elems(self, adding_elements):
        element_branch = self._tree.get(type="branch elems")
        items = []
        for element in adding_elements:
            items.append(element_branch.add(element, type="elem"))
        self.context.signal("element_added", adding_elements)
        return items

    def clear_operations(self):
        operations = self._tree.get(type="branch ops")
        for op in reversed(list(operations.flat(types=("op", "opnode")))):
            if op is not None:
                op.remove_node()

    def clear_elements(self):
        for e in reversed(list(self.elems_nodes())):
            if e is not None:
                e.remove_node()

    def clear_files(self):
        pass

    def clear_elements_and_operations(self):
        self.clear_elements()
        self.clear_operations()

    def clear_all(self):
        self.clear_elements()
        self.clear_operations()
        self.clear_files()
        self.clear_note()
        self.validate_selected_area()

    def clear_note(self):
        self.note = None

    def remove_elements(self, elements_list):
        for elem in elements_list:
            for i, e in enumerate(self.elems()):
                if elem is e:
                    e.node.remove_node()
        self.remove_elements_from_operations(elements_list)
        self.validate_selected_area()

    def remove_operations(self, operations_list):
        for op in operations_list:
            for i, o in enumerate(list(self.ops())):
                if o is op:
                    o.remove_node()
            self.context.signal("operation_removed", op)

    def remove_elements_from_operations(self, elements_list):
        for i, op in enumerate(self.ops()):
            for e in list(op.children):
                if e.object in elements_list:
                    e.remove_node()

    def remove_orphaned_opnodes(self):
        """
        Remove any opnodes whose objects do not appear in the elem list.

        :return:
        """
        elements_list = list(self.elems())
        for i, op in enumerate(self.ops()):
            for e in list(op.children):
                if e.object not in elements_list:
                    e.remove_node()

    def selected_area(self):
        if self._emphasized_bounds_dirty:
            self.validate_selected_area()
        return self._emphasized_bounds

    def validate_selected_area(self):
        boundary_points = []
        for e in self.elems_nodes(emphasized=True):
            if e.bounds is None:
                continue
            box = e.bounds
            top_left = [box[0], box[1]]
            top_right = [box[2], box[1]]
            bottom_left = [box[0], box[3]]
            bottom_right = [box[2], box[3]]
            boundary_points.append(top_left)
            boundary_points.append(top_right)
            boundary_points.append(bottom_left)
            boundary_points.append(bottom_right)

        if len(boundary_points) == 0:
            new_bounds = None
        else:
            xmin = min([e[0] for e in boundary_points])
            ymin = min([e[1] for e in boundary_points])
            xmax = max([e[0] for e in boundary_points])
            ymax = max([e[1] for e in boundary_points])
            new_bounds = [xmin, ymin, xmax, ymax]
        self._emphasized_bounds_dirty = False
        if self._emphasized_bounds != new_bounds:
            self._emphasized_bounds = new_bounds
            self.context.signal("selected_bounds", self._emphasized_bounds)

    def highlight_children(self, node_context):
        """
        Recursively highlight the children.
        :param node_context:
        :return:
        """
        for child in node_context.children:
            child.highlighted = True
            self.highlight_children(child)

    def target_clones(self, node_context, node_exclude, object_search):
        """
        Recursively highlight the children.
        :param node_context:
        :return:
        """
        for child in node_context.children:
            self.target_clones(child, node_exclude, object_search)
            if child is node_exclude:
                continue
            if child.object is None:
                continue
            if object_search is child.object:
                child.targeted = True

    def set_emphasis(self, emphasize):
        """
        If any operation is selected, all sub-operations are highlighted.
        If any element is emphasized, all copies are highlighted.
        If any element is emphasized, all operations containing that element are targeted.
        """
        for s in self._tree.flat():
            if s.highlighted:
                s.highlighted = False
            if s.targeted:
                s.targeted = False

            if s.emphasized:
                if emphasize is None or s not in emphasize:
                    s.emphasized = False
            else:
                if emphasize is not None and (
                    s in emphasize or (hasattr(s, "object") and s.object in emphasize)
                ):
                    s.emphasized = True
        if emphasize is not None:
            for e in emphasize:
                e.emphasized = True
                if hasattr(e, "object"):
                    self.target_clones(self._tree, e, e.object)
                if hasattr(e, "node"):
                    e = e.node
                self.highlight_children(e)

    def center(self):
        bounds = self._emphasized_bounds
        return (bounds[2] + bounds[0]) / 2.0, (bounds[3] + bounds[1]) / 2.0

    def ensure_positive_bounds(self):
        b = self._emphasized_bounds
        if b is None:
            return
        self._emphasized_bounds = [
            min(b[0], b[2]),
            min(b[1], b[3]),
            max(b[0], b[2]),
            max(b[1], b[3]),
        ]
        self.context.signal("selected_bounds", self._emphasized_bounds)

    def update_bounds(self, b):
        self._emphasized_bounds = [b[0], b[1], b[2], b[3]]
        self.context.signal("selected_bounds", self._emphasized_bounds)

    def move_emphasized(self, dx, dy):
        for obj in self.elems(emphasized=True):
            obj.transform.post_translate(dx, dy)
            obj.node.modified()

    def set_emphasized_by_position(self, position):
        def contains(box, x, y=None):
            if y is None:
                y = x[1]
                x = x[0]
            return box[0] <= x <= box[2] and box[1] <= y <= box[3]

        if self.has_emphasis():
            if self._emphasized_bounds is not None and contains(
                self._emphasized_bounds, position
            ):
                return  # Select by position aborted since selection position within current select bounds.
        for e in self.elems_nodes(depth=1, cascade=False):
            try:
                bounds = e.bounds
            except AttributeError:
                continue  # No bounds.
            if bounds is None:
                continue
            if contains(bounds, position):
                e_list = [e]
                self._emphasized_bounds = bounds
                self.set_emphasis(e_list)
                return
        self._emphasized_bounds = None
        self.set_emphasis(None)

    def classify(self, elements, operations=None, add_op_function=None):
        """
        Classify does the placement of elements within operations.

        "Image" is the default for images.

        Typically,
        If element strokes are red they get classed as cut operations
        If they are otherwise they get classed as engrave.
        However, this differs based on the ops in question.

        :param elements: list of elements to classify.
        :param operations: operations list to classify into.
        :param add_op_function: function to add a new operation, because of a lack of classification options.
        :return:
        """

        if elements is None:
            return
        if operations is None:
            operations = list(self.ops())
        if add_op_function is None:
            add_op_function = self.add_op
        for element in elements:
            was_classified = False
            image_added = False
            if hasattr(element, "operation"):
                add_op_function(element)
                continue
            if element is None:
                continue
            for op in operations:
                if op.operation == "Raster":
                    if image_added:
                        continue  # already added to an image operation, is not added here.
                    if element.stroke is not None and op.color == abs(element.stroke):
                        op.add(element, type="opnode")
                        was_classified = True
                    elif isinstance(element, SVGImage):
                        op.add(element, type="opnode")
                        was_classified = True
                    elif element.fill is not None and element.fill.value is not None:
                        op.add(element, type="opnode")
                        was_classified = True
                elif (
                    op.operation in ("Engrave", "Cut")
                    and element.stroke is not None
                    and op.color == abs(element.stroke)
                ):
                    op.add(element, type="opnode")
                    was_classified = True
                elif op.operation == "Image" and isinstance(element, SVGImage):
                    op.add(element, type="opnode")
                    was_classified = True
                    image_added = True
                elif isinstance(element, SVGText):
                    op.add(element)
                    was_classified = True
            if not was_classified:
                if element.stroke is not None and element.stroke.value is not None:
                    op = LaserOperation(
                        operation="Engrave", color=element.stroke, speed=35.0
                    )
                    add_op_function(op)
                    op.add(element, type="opnode")
                    operations.append(op)

    def load(self, pathname, **kwargs):
        kernel = self.context._kernel
        for loader_name in kernel.match("load"):
            loader = kernel.registered[loader_name]
            for description, extensions, mimetype in loader.load_types():
                if str(pathname).lower().endswith(extensions):
                    try:
                        results = loader.load(self.context, self, pathname, **kwargs)
                    except FileNotFoundError:
                        return False
                    if not results:
                        continue
                    return True

    def load_types(self, all=True):
        kernel = self.context._kernel
        filetypes = []
        if all:
            filetypes.append("All valid types")
            exts = []
            for loader_name in kernel.match("load"):
                loader = kernel.registered[loader_name]
                for description, extensions, mimetype in loader.load_types():
                    for ext in extensions:
                        exts.append("*.%s" % ext)
            filetypes.append(";".join(exts))
        for loader_name in kernel.match("load"):
            loader = kernel.registered[loader_name]
            for description, extensions, mimetype in loader.load_types():
                exts = []
                for ext in extensions:
                    exts.append("*.%s" % ext)
                filetypes.append("%s (%s)" % (description, extensions[0]))
                filetypes.append(";".join(exts))
        return "|".join(filetypes)

    def save(self, pathname):
        kernel = self.context._kernel
        for save_name in kernel.match("save"):
            saver = kernel.registered[save_name]
            for description, extension, mimetype in saver.save_types():
                if pathname.lower().endswith(extension):
                    saver.save(self.context, pathname, "default")
                    return True
        return False

    def save_types(self):
        kernel = self.context._kernel
        filetypes = []
        for save_name in kernel.match("save"):
            saver = kernel.registered[save_name]
            for description, extension, mimetype in saver.save_types():
                filetypes.append("%s (%s)" % (description, extension))
                filetypes.append("*.%s" % (extension))
        return "|".join(filetypes)
