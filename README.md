# FRAME_INFO

## Formatting

By default there are

-   autopep8 for Python files
-   prettier for other files
-   docformatter for docstrings

Command line:

Source:
`$ autopep8 --in-place .`

Docstrings:
`$ docformatter --wrap-summaries 88 --wrap-descriptions 88 --in-place <filepath>`

## Tests

$ python -m unittest