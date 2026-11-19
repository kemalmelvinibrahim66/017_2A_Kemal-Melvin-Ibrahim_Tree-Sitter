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

    _expr: $ => choice($.comparison, $.and_expression),

    comparison: $ => seq(
      $.identifier,
      choice('=', '!=', '>', '<', '>=', '<='),
      $._value
    ),

    and_expression: $ => prec.left(2, seq($._expr, 'and', $._expr)),
    
    _value: $ => choice($.string, $.number),
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
  }
});
