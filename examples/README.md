# Examples

## Input Format

The file `input.txt` should provide a working example of what the tool expects.

Its format is very straightforward; it should be a comma-delimited file with three columns. The title is the first one; it is only for diplay purposes and has no role in the insertion of the rules. The base URL is the second one; it should be relative and contain a leading forward slash `/`. The vanity URL is the last one and it is optional; this column is pipe delimited `|`, so that multiple URLs can be passed.

### Example

Title | Base URL | Vanity URL
:--- | :--- | :---
`Premios Billboard` | `/entretenimiento/premios_billboard` | `/billboard|/billboard2014`

## Output Format

The files `output.txt` should provide a working example of what the tool outputs.

Its format is attuned to what `telemundo/murtl` expects as input; which is a tab-delimited file with 4 to 5 columns, depending on the type of redirect rule.

### Examples

#### Static

Title | Type | Source | Destination
:--- | :--- | :--- | :--- 
`Vanity` | `static` | `http://www.telemundo.com/billboard` | `http://movil.telemundo.com/entretenimiento/premios_billboard`

#### Dynamic

Title | Type | Source | Destination | Regex (PHP)
:--- | :--- | :--- | :--- | :---
`Article` | `advanced` | `http://www.telemundo.com/entretenimiento/premios_billboard/article/` | `http://movil.telemundo.com/\1/\2` | `#/([a-z0-9_]+)/(.*)#i`

#### Do Not Redirect

Title | Type | Source | Redirect
:--- | :--- | :--- | :--- | :--- 
`Vanity (DNR)` | `passthru` | `http://www.telemundo.com/billboard` | `3`