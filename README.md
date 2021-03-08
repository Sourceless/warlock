# warlock
Practical magic for everyday programmers.

## Features
None of this is implemented!
* Two languages - a language that looks like python, designed to be easy to read and write, and a language that is easy to execute and write macros for
* Dependent types - first class functions and types
* Macros - the ability to alter the syntax however you need to build a language for your domain
* Immutability. All variables are immutable.

## The languages
### Warlock
`warlock` is the main, good-looking language. It is purposefully modelled after python,
primarily because it's a Very Readable Language. However, the resemblance is only skin deep.

### Wizard
`wizard` is ugly (well, beautiful to me), but perfectly formed for easy execution and macros. It's a LISP-2, and you can think of `warlock` as an M-Expression form of `wizard`.

## Toolchain
```
offside tokenizer -> warlock parser -> wizard generator -> wizard interpreter/compiler
```

### Offside tokenizer
Implements the 'offside rule' for warlock, making it parseable using context-free grammars.

### Warlock parser
Produces an AST for a warlock program that has been run through the offside tokenizer.

### Wizard generator
Generates a wizard program from a warlock AST.

### Wizard interpreter/compiler
The final step, where the wizard program is either executed or made into an executable.

## Inspirations
* Python (& Hy)
* Clojure
* Idris/Coq
