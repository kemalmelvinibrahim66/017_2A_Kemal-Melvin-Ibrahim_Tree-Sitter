/**
 * @file DSL filter
 * @author Kemal Melvin Ibrahim <kemal.melvin.tif425@polban.ac.id>
 * @license MIT
 */

export default grammar({
  name: 'filter',
  extras: $ => [/\s/],
  word: $ => $.identifier,

  rules: {
    query: $ => $._expr,

    _expr: $ => choice($.comparison, $.and_expression, $.or_expression, $.parenthesized, $.not_expression),
    comparison: $ => seq(
    field('field', $.identifier),
    field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
    field('value', $._value),
  ),

    and_expression: $ => prec.left(2, seq(field('left', $._expr), 'and', field('right', $._expr))),
    or_expression: $ => prec.left(1, seq(field('left', $._expr), 'or', field('right', $._expr))),
    parenthesized: $ => seq('(', $._expr, ')'),
    not_expression: $ => prec(3, seq('not', field('operand', $._expr))),
    
    _value: $ => choice($.string, $.number, $.boolean),
    boolean: $ => choice('true', 'false'),
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
  }
});
