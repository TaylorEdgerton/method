# Expression Language Reference

## Table of Contents
- [Basic Syntax](#basic-syntax)
- [Reference Types](#reference-types)
- [Comparison Functions](#comparison-functions)
- [Math Functions](#math-functions)
- [String Functions](#string-functions)
- [Date/Time Functions](#datetime-functions)
- [Quality Functions](#quality-functions)
- [Advanced Functions](#advanced-functions)
- [Common Patterns](#common-patterns)

## Basic Syntax

### Reference Types
```
{[provider]path/to/tag}           # Tag reference
{[provider]path/to/tag.property}  # Tag property (engHigh, engLow, etc.)
{this.props.propertyName}         # Component property
{this.custom.customProp}          # Component custom property
{view.params.paramName}           # View parameter
{view.custom.customProp}          # View custom property
{session.props.user.username}     # Session property
{session.custom.customProp}       # Session custom property
```

### Tag Property Access
```
{[default]MyTag}                  # Tag value
{[default]MyTag.engHigh}          # Engineering high
{[default]MyTag.engLow}           # Engineering low
{[default]MyTag.quality}          # Tag quality
{[default]MyTag.timestamp}        # Last change time
{[default]MyTag.dataType}         # Data type
```

## Comparison Functions

```
if(condition, trueValue, falseValue)
# Nested: if(cond1, val1, if(cond2, val2, val3))

# Comparison operators
=, !=, <, >, <=, >=, like, not like

# Logical operators
and, or, not, &&, ||, !

# Examples
if({[default]Level} > 80, "HIGH", "NORMAL")
if({[default]Status} = 1 and {[default]Running}, "Active", "Inactive")
```

### Switch/Case Alternative
```
# Using nested if for case-like behavior
if({[default]State} = 0, "Stopped",
  if({[default]State} = 1, "Running",
    if({[default]State} = 2, "Fault", "Unknown")))

# Using choose() for index-based selection
choose({[default]Index}, "Zero", "One", "Two", "Three")
```

## Math Functions

```
abs(value)                    # Absolute value
ceiling(value)                # Round up
floor(value)                  # Round down
round(value, decimals)        # Round to decimals
max(a, b, ...)               # Maximum value
min(a, b, ...)               # Minimum value
sqrt(value)                   # Square root
pow(base, exponent)          # Power
mod(dividend, divisor)       # Modulo
log(value)                    # Natural log
log10(value)                  # Log base 10

# Examples
round({[default]Temperature}, 1)
max({[default]Tank1/Level}, {[default]Tank2/Level})
```

## String Functions

```
len(string)                           # Length
upper(string)                         # Uppercase
lower(string)                         # Lowercase
trim(string)                          # Remove whitespace
left(string, count)                   # Left characters
right(string, count)                  # Right characters
substring(string, start, end)         # Substring (0-indexed)
replace(string, search, replace)      # Replace text
concat(str1, str2, ...)              # Concatenate
split(string, delimiter, index)       # Split and get part
indexOf(string, search)               # Find position (-1 if not found)
contains(string, search)              # Boolean contains
startsWith(string, prefix)            # Boolean starts with
endsWith(string, suffix)              # Boolean ends with

# Formatting
stringFormat(pattern, arg1, arg2, ...)
numberFormat(value, pattern)
dateFormat({timestamp}, pattern)

# Examples
stringFormat("Tank %d: %.1f%%", {[default]TankID}, {[default]Level})
numberFormat({[default]Value}, "#,##0.00")
upper(left({[default]ProductCode}, 3))
```

## Date/Time Functions

```
now(interval_ms)                      # Current time, updates at interval
getDate(year, month, day)            # Create date
getTime(hour, min, sec)              # Create time
addHours(date, hours)                # Add hours
addMinutes(date, minutes)            # Add minutes
addDays(date, days)                  # Add days
addMonths(date, months)              # Add months
addYears(date, years)                # Add years
diffHours(date1, date2)              # Hours between
diffMinutes(date1, date2)            # Minutes between
diffDays(date1, date2)               # Days between
diffSeconds(date1, date2)            # Seconds between
getHour(date)                        # Extract hour (0-23)
getMinute(date)                      # Extract minute
getSecond(date)                      # Extract second
getDayOfWeek(date)                   # Day of week (1=Sun, 7=Sat)
getDayOfMonth(date)                  # Day of month (1-31)
getMonth(date)                       # Month (1-12)
getYear(date)                        # Year

# Formatting patterns
dateFormat({timestamp}, "yyyy-MM-dd HH:mm:ss")
dateFormat({timestamp}, "MMM d, yyyy")
dateFormat({timestamp}, "HH:mm")

# Examples
diffMinutes(now(1000), {[default]LastUpdate})
dateFormat(addDays(now(60000), -7), "yyyy-MM-dd")
```

## Quality Functions

```
isGood(tagValue)                     # True if quality is good
isBad(tagValue)                      # True if quality is bad
isUncertain(tagValue)                # True if quality is uncertain
hasChanged(tagValue, type)           # True if changed (types: "Value", "Quality", "Timestamp")
coalesce(val1, val2, ..., default)   # First non-null value

# Quality-aware expressions
if(isGood({[default]Tag}), {[default]Tag}, "N/A")
coalesce({[default]Primary}, {[default]Backup}, 0)
```

## Advanced Functions

### Type Conversion
```
toInt(value)                         # Convert to integer
toFloat(value)                       # Convert to float  
toStr(value)                         # Convert to string
toBool(value)                        # Convert to boolean
toColor(r, g, b)                     # Create color
toColor(r, g, b, a)                  # Create color with alpha
```

### Dataset Functions (Vision)
```
lookup(dataset, keyColumn, keyValue, resultColumn)
runScript(scriptPath, pollRate, args...)
tag(tagPath)                         # Explicit tag reference
```

### Translation
```
translate(key)                       # Translate key
translate(key, arg1, arg2)          # Translate with arguments
```

### Binomial Bound
```
binomLower(trials, successes, confidence)
binomUpper(trials, successes, confidence)
```

## Common Patterns

### Status Indicator Color
```
if({[default]Status} = "Running", toColor(0, 200, 0),
  if({[default]Status} = "Fault", toColor(255, 0, 0),
    if({[default]Status} = "Stopped", toColor(128, 128, 128),
      toColor(255, 165, 0))))
```

### Range Mapping (Level to Color)
```
if({[default]Level} > 90, toColor(255, 0, 0),
  if({[default]Level} > 70, toColor(255, 165, 0),
    if({[default]Level} > 30, toColor(0, 200, 0),
      toColor(0, 100, 255))))
```

### Elapsed Time Display
```
# Minutes since event
stringFormat("%.0f min ago", diffMinutes(now(60000), {[default]LastEvent}))

# Hours:Minutes format
stringFormat("%d:%02d", 
  floor(diffMinutes(now(1000), {[default]StartTime})/60),
  mod(floor(diffMinutes(now(1000), {[default]StartTime})), 60))
```

### Safe Division
```
if({[default]Denominator} != 0, 
  {[default]Numerator} / {[default]Denominator}, 
  0)
```

### Percentage Calculation
```
round(({[default]Current} - {[default]Min}) / 
      ({[default]Max} - {[default]Min}) * 100, 1)
```

### Alarm Severity Text
```
choose({[default]AlarmSeverity}/250 + 1,
  "Low", "Medium", "High", "Critical")
```

### Dynamic Tag Path
```
# Use indirect binding type instead of expression for dynamic paths
# In expression, tag paths must be static
```

### Boolean to Text
```
if({[default]Running}, "ON", "OFF")
if({[default]AutoMode}, "AUTO", "MANUAL")
```

### Null/Quality Handling
```
# Provide default for bad quality
if(isGood({[default]Value}), round({[default]Value}, 2), "---")

# First available value
coalesce({[default]Primary}, {[default]Backup}, {[default]Default})
```
