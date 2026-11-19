/**
 * @file DSL filter
 * @author Kemal Melvin Ibrahim <kemal.melvin.tif425@polban.ac.id>
 * @license MIT
 */

export default grammar({
  name: 'filter',
  extras: $ => [/\s/],

  rules: {
    query: $ => $.comparison,
    comparison: $ => seq(
      $.identifier,
      choice('=', '!=', '>', '<', '>=', '<='),
      $._value
    ),
    _value: $ => choice($.string, $.number),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    number: $ => /\d+(\.\d+)?/,
    string: $ => /"[^"]*"/,
  }
});
