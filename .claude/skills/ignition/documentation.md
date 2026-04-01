# Ignition Documentation Reference

## Primary Documentation Sources

### Official Documentation (Inductive Automation)
Base URL: `https://docs.inductiveautomation.com/docs/8.1/`

| Topic | URL Path |
|-------|----------|
| Getting Started | `getting-started/quick-start` |
| Perspective | `perspective` |
| Vision | `vision` |
| Tags | `platform/tags` |
| Alarming | `platform/alarming` |
| Historical Data | `platform/history` |
| Scripting Functions | `appendix/scripting-functions` |
| Expression Functions | `appendix/expression-functions` |
| Named Queries | `platform/data/named-queries` |
| Security | `platform/security` |
| Projects | `platform/projects` |

### Web Search Queries
Use these search patterns to find documentation:

```
# General topics
"Ignition 8.1 [topic]"
"Ignition Perspective [component name]"
"Ignition system.[namespace] function"

# Specific functions
"Ignition system.tag.readBlocking"
"Ignition system.perspective.navigate"
"Ignition expression if function"

# Components
"Ignition Perspective Table component"
"Ignition Vision Easy Chart"

# Troubleshooting
"Ignition [error message]"
"Ignition forum [problem description]"
```

## Scripting Function Reference URLs

### system.* Namespaces
| Namespace | Documentation URL |
|-----------|------------------|
| system.tag | `appendix/scripting-functions/system-tag` |
| system.db | `appendix/scripting-functions/system-db` |
| system.date | `appendix/scripting-functions/system-date` |
| system.dataset | `appendix/scripting-functions/system-dataset` |
| system.util | `appendix/scripting-functions/system-util` |
| system.alarm | `appendix/scripting-functions/system-alarm` |
| system.perspective | `appendix/scripting-functions/system-perspective` |
| system.gui | `appendix/scripting-functions/system-gui` |
| system.nav | `appendix/scripting-functions/system-nav` |
| system.file | `appendix/scripting-functions/system-file` |
| system.net | `appendix/scripting-functions/system-net` |
| system.opc | `appendix/scripting-functions/system-opc` |
| system.report | `appendix/scripting-functions/system-report` |
| system.serial | `appendix/scripting-functions/system-serial` |
| system.sfc | `appendix/scripting-functions/system-sfc` |
| system.user | `appendix/scripting-functions/system-user` |
| system.print | `appendix/scripting-functions/system-print` |
| system.bacnet | `appendix/scripting-functions/system-bacnet` |
| system.dnp3 | `appendix/scripting-functions/system-dnp3` |
| system.iec61850 | `appendix/scripting-functions/system-iec61850` |
| system.kanoa | `appendix/scripting-functions/system-kanoa` |
| system.mes | `appendix/scripting-functions/system-mes` |

## Perspective Component Reference

Base URL: `https://docs.inductiveautomation.com/docs/8.1/perspective/perspective-component-reference/`

### Container Components
- `perspective-containers/flex-container`
- `perspective-containers/column-container`
- `perspective-containers/coordinate-container`
- `perspective-containers/tab-container`
- `perspective-containers/split-container`
- `perspective-containers/breakpoint-container`

### Display Components
- `perspective-displays/label`
- `perspective-displays/value-display`
- `perspective-displays/icon`
- `perspective-displays/image`
- `perspective-displays/embedded-view`
- `perspective-displays/table`
- `perspective-displays/markdown`

### Input Components
- `perspective-inputs/button`
- `perspective-inputs/text-field`
- `perspective-inputs/numeric-entry-field`
- `perspective-inputs/dropdown`
- `perspective-inputs/checkbox`
- `perspective-inputs/radio-group`
- `perspective-inputs/slider`
- `perspective-inputs/date-time-picker`

### Chart Components
- `perspective-charts/xy-chart`
- `perspective-charts/pie-chart`
- `perspective-charts/bar-chart`
- `perspective-charts/power-chart`
- `perspective-charts/sparkline`

### Symbol Components
- `perspective-symbols/symbol`
- `perspective-symbols/cylindrical-tank`
- `perspective-symbols/horizontal-tank`
- `perspective-symbols/spherical-tank`
- `perspective-symbols/pipes`
- `perspective-symbols/valve`
- `perspective-symbols/motor`
- `perspective-symbols/pump`

## Expression Functions Reference

URL: `https://docs.inductiveautomation.com/docs/8.1/appendix/expression-functions/`

Categories:
- `expression-functions-comparison`
- `expression-functions-math`
- `expression-functions-string`
- `expression-functions-date-time`
- `expression-functions-quality`
- `expression-functions-conversion`
- `expression-functions-color`
- `expression-functions-logic`

## Community Resources

### Inductive Automation Forum
URL: `https://forum.inductiveautomation.com/`

Search patterns:
```
site:forum.inductiveautomation.com [search terms]
site:forum.inductiveautomation.com Perspective [component]
site:forum.inductiveautomation.com Python [function]
```

### Inductive University (Training)
URL: `https://inductiveuniversity.com/`

### GitHub Examples
- `github.com/inductiveautomation` - Official examples
- Search: `github.com ignition perspective`

## Version-Specific Documentation

For different Ignition versions, adjust the version in the URL:
- 8.1: `docs/8.1/`
- 8.0: `docs/8.0/`
- 7.9: `docs/7.9/`

Check the Ignition version in the project to use correct documentation.

## Lookup Strategy

When encountering unfamiliar concepts:

1. **Function lookup**: Search `"Ignition system.[namespace].[function]"`
2. **Component lookup**: Search `"Ignition Perspective [component name] props"`
3. **Expression lookup**: Search `"Ignition expression [function name]"`
4. **Error lookup**: Search the exact error message with `"Ignition"`
5. **Pattern lookup**: Search `"Ignition [what you want to do] example"`

## API/JSON Structure Discovery

When documentation is insufficient:
1. Export existing working configuration from Ignition Designer
2. Examine the JSON structure in exported files
3. Use Designer's Script Console to explore:
   ```python
   # List available methods
   dir(system.tag)
   
   # Get function help
   help(system.tag.readBlocking)
   ```

## Quick Reference Cards

### Most Common Functions
```python
# Tags
system.tag.readBlocking([paths])
system.tag.writeBlocking([paths], [values])
system.tag.browse(path)

# Database
system.db.runNamedQuery(path, params)
system.db.runPrepQuery(query, args, database)

# Perspective
system.perspective.navigate(view, params)
system.perspective.openPopup(id, view, params)
system.perspective.sendMessage(messageType, payload, scope)

# Vision
system.gui.openWindow(name)
system.nav.swapWindow(old, new)
system.gui.getWindow(name)

# Utility
system.util.getLogger(name)
system.date.now()
system.date.format(date, pattern)
system.dataset.toPyDataSet(dataset)
```

### Most Common Expressions
```
{[provider]path/to/tag}           # Tag reference
if(condition, true, false)        # Conditional
coalesce(val1, val2, default)    # First non-null
stringFormat(pattern, args...)    # String formatting
dateFormat(date, pattern)         # Date formatting
round(value, decimals)            # Round number
```
