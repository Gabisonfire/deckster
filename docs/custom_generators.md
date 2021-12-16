# Custom generators
Custom generators are simply Python modules, just like plugins but they are executed before the keys config are loaded.

Generators' entry points must be a function called `main` and must receive 1 argument: `args`.

- `args`: Is the content of the generators `args` portion in the `config.json`.