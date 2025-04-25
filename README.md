# 🛠️ cpy Compiler
Build a fully functional compiler for the cpy language in Python.


## 📘 Language Description

The `cpy` language is a small programming language designed for educational purposes, specifically for compiler construction assignments. Although its programming capabilities are limited, `cpy` includes key features such as functions, parameter passing, recursive calls, and nested function declarations. This makes the implementation of its compiler educationally valuable and interesting.

On the other hand, `cpy` deliberately omits several common programming constructs such as the `for` loop, floating-point numbers, strings, and arrays. These omissions are made solely to reduce the code complexity, without compromising the educational challenge or value of the assignment.

## 🔤 Lexical Elements

The alphabet of `cpy` includes:
- Uppercase and lowercase Latin letters (A–Z, a–z)
- Digits (0–9)
- Arithmetic operators: `+`, `-`, `*`, `//`, `%`
- Relational operators: `<`, `>`, `==`, `<=`, `>=`, `!=`
- Assignment operator: `=`
- Separators: `,`, `:`
- Grouping symbols: `(`, `)`, `#{`, `#}`
- Comment delimiters: `##`

### 🚫 Reserved Words

main, def, #def, #int, global,
if, elif, else, while,
print, return, input, int,
and, or, not

# cpy Language Specifications

## Reserved Words

These words cannot be used as variables.

## Constants

The constants of the language are integer constants composed of an optional sign and a sequence of numeric digits.

## Identifiers

The identifiers of the language are strings composed of letters and digits, but they must start with a letter. The compiler only considers the first thirty letters.

## Whitespace

Whitespace characters (tab, space, return) are ignored and can be used in any way without affecting the operation of the compiler, as long as they are not within reserved words, identifiers, or constants.

## Comments

The same applies to comments, which must be enclosed between the symbols `##`. Nested comments are not supported.

## Types and Variable Declarations

The only data type supported by cpy is integers. The integers must have values from –32767 to 32767. Declarations are made with the command `#int`. Following are the names of the identifiers without any other declaration, since we know they are integer variables, and they do not need to be on the same line. Variables are separated by commas. More than one consecutive use of `#int` is allowed.

## Operators and Expressions

The priority of operators from highest to lowest is:

1. Unary logical: `not`
2. Multiplicative: `*`, `//`, `%`
3. Unary additive: `+`, `-`
4. Binary additive: `+`, `-`
5. Relational: `==`, `<`, `>`, `!=`, `<=`, `>=`
6. Logical: `and`
7. Logical: `or`


Language Structures

Assignment
The assignment statement id = expression is used to assign the value of a variable, constant, or an expression to a variable.

Decision (if)
if condition:
    statements1
[elif condition:
    statements2]*
[else:
    statements3]
The if statement evaluates whether the condition is true. If it is true, the statements following it are executed. If the condition is false, the conditions next to each elif are checked one by one. For the first elif that evaluates as true, the corresponding statements2 are executed. If none of the elif conditions are true, then the statements3 corresponding to the else will be executed. The elif and else parts are optional, which is why they are enclosed in square brackets.

Loop (while)

while condition:
    statements
The while loop repeats the statements as long as the condition is true. If the first evaluation of the condition is false, the statements will not be executed.

Function Return
return expression
Used inside functions to return the result of the function.

Output
print(expression)
Displays the result of evaluating the expression on the screen.

Input
id = int(input())
Requests the user to provide a value via the keyboard.

Functions
Cpy supports functions.

def id(formal_pars):
{
    declarations
    globals
    functions
    code_block
}
formal_pars is the list of formal parameters. Functions can be nested within each other, and the scoping rules are similar to those in PASCAL. The return value of a function is provided using return.

A function call is made from arithmetic expressions as an operator, for example:

D = a + f(x)
Where f is the function and x is the parameter passed by value.

Global variables are declared at the beginning of the program with the keyword #int. Any function that wishes to access a global variable must re-declare it locally using the global keyword.

Parameter Passing
Cpy supports parameter passing similar to Python.

File Extension
Cpy files have the .cpy extension.

