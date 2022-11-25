from __future__ import annotations

import ast
import inspect
import logging
import sys
import types
from typing import Any
from typing_extensions import Annotated, TypeGuard
from .QuantityNode import QuantityNode
from pint import UnitRegistry
import pint

annot_type = type(Annotated[int, "spam"])

_log = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def is_annotated(hint: Any, annot_type=annot_type) -> TypeGuard[annot_type]:
    return (type(hint) is annot_type) and hasattr(hint, "__metadata__")


class AstRaise(ast.NodeTransformer):
    def get_node(self, except_name: str) -> ast.Raise:
        mod = ast.parse(f"raise {except_name}")
        self.generic_visit(mod)
        return self.exception

    def visit_Raise(self, node: ast.Raise):
        self.exception = node


def raise_dim_error(e, received, expected):
    exception = (
        e.__module__ + "." + e.__qualname__ + f'("{received}", "{expected}")'
    )
    new_node = AstRaise().get_node(exception)
    return new_node


class Visitor(ast.NodeTransformer):
    couscous_func: dict[str, inspect.Signature] = {}
    ureg = UnitRegistry()

    @classmethod
    def add_func(cls, fun):
        cls.couscous_func[fun.__name__] = inspect.signature(fun)

    def __init__(self, fun) -> None:
        self.fun_globals = fun.__globals__
        self.mod = sys.modules[fun.__module__]
        self.add_func(fun)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.vars = {}
        self.calls = {}

        # Adding all annotations from own module
        annotations = getattr(self.mod, "__annotations__", None)
        if annotations is not None:
            for name, anno in annotations.items():
                if is_annotated(anno):
                    self.vars[name] = anno.__metadata__[0]
                if isinstance(anno, str):
                    self.vars[name] = anno

        # Adding all annotations from imported modules
        for _, val in self.fun_globals.items():
            if isinstance(val, types.ModuleType):
                annotations = getattr(val, "__annotations__", None)
                if annotations is not None:
                    for name, anno in annotations.items():
                        if is_annotated(anno):
                            self.vars[name] = anno.__metadata__[0]
                        if isinstance(anno, str):
                            self.vars[name] = anno

        for arg in node.args.args:
            annotation = getattr(arg, "annotation", None)
            if annotation is not None:
                if isinstance(annotation, ast.Constant):
                    if annotation.value in self.ureg:
                        self.vars[arg.arg] = arg.annotation.value
                    else:
                        _log.warning(
                            "Signature of couscoussed functions must be in Unit Registry"
                        )
                elif isinstance(annotation, ast.Subscript):
                    if annotation.value.id == "Annotated":
                        self.vars[arg.arg] = arg.annotation.slice.value.elts[
                            1
                        ].value
                else:
                    _log.warning(
                        "Signature of couscoussed functions must be of type string or typing.Annotated"
                    )
        self.generic_visit(node)
        return node

    def get_node_unit(self, node: ast.AST) -> QuantityNode:
        """Method to induce the unit of a node through recursive
        calls on children if any.

        Args:
            node (ast.AST): input node

        Returns:
            QuantityNode: QuantityNode(node, induced_unit)
        """

        if isinstance(node, ast.Constant):
            return QuantityNode(node, None)
        elif isinstance(node, ast.Tuple):
            elems = list(map(self.get_node_unit, node.elts))
            return QuantityNode(
                ast.Tuple([elem.node for elem in elems], ctx=node.ctx),
                [elem.unit for elem in elems],
            )
        elif isinstance(node, ast.List):
            return list(map(self.get_node_unit, node.elts))
        elif isinstance(node, ast.Set):
            return set(map(self.get_node_unit, node.elts))
        elif isinstance(node, ast.Dict):
            return dict(
                zip(
                    map(self.get_node_unit, node.keys),
                    map(self.get_node_unit, node.values),
                )
            )
        elif isinstance(node, ast.Name):
            return QuantityNode(node, self.vars[node.id])

        elif isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Sub)
        ):
            left = self.get_node_unit(node.left)
            right = self.get_node_unit(node.right)

            if left.unit is None or right.unit is None:
                new_node = ast.BinOp(left.node, node.op, right.node)
                ast.copy_location(new_node, node)
                return QuantityNode(new_node, None)

            if pint.Unit(left.unit).is_compatible_with(pint.Unit(right.unit)):
                conv_value = pint.Unit(left.unit).from_(pint.Unit(right.unit)).m
                new_node = ast.BinOp(
                    left.node,
                    node.op,
                    ast.BinOp(right.node, ast.Mult(), ast.Constant(conv_value)),
                )
                ast.copy_location(new_node, node)
                return QuantityNode(new_node, left.unit)

            else:
                raise_node = raise_dim_error(
                    pint.errors.DimensionalityError, right.unit, left.unit
                )
                ast.copy_location(raise_node, node)
                return QuantityNode(raise_node, "dimensionless")

        elif isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Mult, ast.Div)
        ):
            left = self.get_node_unit(node.left)
            right = self.get_node_unit(node.right)

            if left.unit is None or right.unit is None:
                new_node = ast.BinOp(left.node, node.op, right.node)
                ast.copy_location(new_node, node)
                return QuantityNode(new_node, None)

            if pint.Unit(left.unit).is_compatible_with(pint.Unit(right.unit)):
                conv_value = pint.Unit(left.unit).from_(pint.Unit(right.unit)).m
                new_node = ast.BinOp(
                    left.node,
                    node.op,
                    ast.BinOp(right.node, ast.Mult(), ast.Constant(conv_value)),
                )
                ast.copy_location(new_node, node)
                unit = (
                    f"{left.unit}*{left.unit}"
                    if isinstance(node.op, ast.Mult)
                    else "dimensionless"
                )
                return QuantityNode(new_node, unit)

            else:
                new_node = ast.BinOp(left.node, node.op, right.node)
                ast.copy_location(new_node, node)
                unit = (
                    f"{left.unit}*{right.unit}"
                    if isinstance(node.op, ast.Mult)
                    else f"{left.unit}/{right.unit}"
                )
                return QuantityNode(new_node, unit)

        elif isinstance(node, ast.BinOp):
            return QuantityNode(node, self.get_node_unit(node.left).unit)

        elif isinstance(node, ast.Call):

            id = (
                node.func.id
                if isinstance(node.func, ast.Name)
                else node.func.attr
            )
            if id in self.couscous_func:
                signature = self.couscous_func[id]
            else:
                signature = inspect.Signature(
                    parameters=None, return_annotation=None
                )

            new_args = []
            for i, (_, param) in enumerate(signature.parameters.items()):

                expected = param.annotation

                if (received := self.get_node_unit(node.args[i]).unit) == None:
                    _log.warning(
                        f"Function {id} expected unit {expected} but received unitless quantity"
                    )
                    continue
                if received != expected:

                    if expected is inspect._empty:
                        pass
                    else:
                        if pint.Unit(received).is_compatible_with(
                            pint.Unit(expected)
                        ):
                            conv_value = (
                                pint.Unit(expected).from_(pint.Unit(received)).m
                            )
                        else:
                            raise_node = raise_dim_error(
                                pint.errors.DimensionalityError,
                                received,
                                expected,
                            )
                            return QuantityNode(raise_node, "dimensionless")

                        new_arg = ast.BinOp(
                            node.args[i],
                            ast.Mult(),
                            ast.Constant(conv_value),
                        )
                        new_args.append(new_arg)

            new_node = (
                node
                if not new_args
                else ast.Call(
                    func=node.func,
                    args=new_args,
                    keywords=node.keywords,
                )
            )

            ast.copy_location(new_node, node)
            return QuantityNode(new_node, signature.return_annotation)

        elif isinstance(node, ast.Attribute):
            return QuantityNode(node, self.vars[node.attr])

    def visit_Call(self, node: ast.Call) -> Any:

        if isinstance(node.func, ast.Name):

            if node.func.id in __builtins__.keys():
                return node

            signature = inspect.signature(self.fun_globals[node.func.id])
            new_args = []
            for i, (_, value) in enumerate(signature.parameters.items()):
                if (received := self.get_node_unit(node.args[i]).unit) != (
                    expected := value.annotation
                ):
                    if pint.Unit(received).is_compatible_with(
                        pint.Unit(expected)
                    ):
                        conv_value = (
                            pint.Unit(expected).from_(pint.Unit(received)).m
                        )
                    else:
                        raise_node = raise_dim_error(
                            pint.errors.DimensionalityError, received, expected
                        )
                        return raise_node

                    new_arg = ast.BinOp(
                        node.args[i],
                        ast.Mult(),
                        ast.Constant(conv_value),
                    )
                    new_args.append(new_arg)

            if new_args:
                new_node = ast.Call(
                    func=node.func,
                    args=new_args,
                    keywords=node.keywords,
                )
                ast.copy_location(new_node, node)
                ast.fix_missing_locations(new_node)

                return new_node

        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:

        value = self.get_node_unit(node.value)

        if value.node != node.value:
            node = ast.AnnAssign(
                target=node.target,
                annotation=node.annotation,
                value=value.node,
                simple=node.simple,
            )

        if value.unit is None:
            _log.warning(f"The unit of {node.target.id} could not be checked.")
            new_node = node

        elif (received := value.unit) != (expected := node.annotation.value):
            if received == "dimensionless":
                new_node = node
            elif pint.Unit(received).is_compatible_with(pint.Unit(expected)):
                conv_value = pint.Unit(expected).from_(pint.Unit(received)).m
                new_value = ast.BinOp(
                    node.value,
                    ast.Mult(),
                    ast.Constant(conv_value),
                )
                new_node = ast.AnnAssign(
                    target=node.target,
                    annotation=node.annotation,
                    value=new_value,
                    simple=node.simple,
                )

            else:
                raise_node = raise_dim_error(
                    pint.errors.DimensionalityError, received, expected
                )
                return raise_node
        else:
            new_node = node

        self.vars[node.target.id] = node.annotation.value
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        return self.get_node_unit(node).node

    def visit_Assign(self, node: ast.Assign) -> Any:

        value = self.get_node_unit(node.value)

        if value.node != node.value:
            node = ast.Assign(
                targets=node.targets,
                value=value.node,
            )

        if isinstance(node.value, ast.Call):
            for target in node.targets:
                if isinstance(target, ast.Tuple):
                    for i, elem in enumerate(target.elts):
                        self.vars[elem.id] = (
                            inspect.signature(
                                self.fun_globals[node.value.func.id]
                            )
                            .return_annotation.__args__[i]
                            .__forward_value__
                        )
                else:
                    self.vars[target.id] = value.unit

            new_node = node

        else:
            new_node = ast.Assign(
                targets=node.targets,
                value=value.node,
                type_comment=f"unit: {value.unit}",
            )
            for target in node.targets:
                if isinstance(target, ast.Tuple):
                    for i, elem in enumerate(target.elts):
                        self.vars[elem.id] = value.unit[i]
                else:
                    self.vars[target.id] = value.unit

        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node
