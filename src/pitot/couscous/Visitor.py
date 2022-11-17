from __future__ import annotations

import ast
import inspect
import logging
from typing import Any
import warnings
from .QuantityNode import QuantityNode
from pint import UnitRegistry
import pint


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
    def __init__(self, fun_globals) -> None:
        self.fun_globals = fun_globals
        self.ureg = UnitRegistry()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.vars = {}
        self.calls = {}

        for arg in node.args.args:
            self.vars[arg.arg] = (
                arg.annotation.value
                if arg.annotation is not None
                else "dimensionless"
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
            return QuantityNode(node, "dimensionless")
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
                return raise_node

        elif isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Mult, ast.Div)
        ):
            left = self.get_node_unit(node.left)
            right = self.get_node_unit(node.right)

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

        elif isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):
                signature = inspect.signature(self.fun_globals[node.func.id])
            elif isinstance(node.func, ast.Attribute):
                signature = inspect.signature(
                    getattr(
                        self.fun_globals[node.func.value.id],
                        node.func.attr,
                    ).__call__
                )

            unit = (
                signature.return_annotation
                if signature.return_annotation is not inspect._empty
                else "dimensionless"
            )

            new_args = []
            for i, (_, value) in enumerate(signature.parameters.items()):
                if (received := self.get_node_unit(node.args[i]).unit) != (
                    expected := value.annotation
                ):
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
                            return raise_node

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
            return QuantityNode(new_node, unit)

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

        if (received := value.unit) != (expected := node.annotation.value):
            if pint.Unit(received).is_compatible_with(pint.Unit(expected)):
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
                # TODO : Warning for a dimension discrepancy
                warnings.warn("Bad bad units")
                new_node = node
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
