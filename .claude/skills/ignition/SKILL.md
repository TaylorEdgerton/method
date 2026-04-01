---
name: ignition-scada
description: |
  Ignition SCADA development expert for Perspective and Vision modules. Use when working with:
  (1) Ignition project JSON files (view.json, resource.json, project.json)
  (2) Tag configuration files (tags.json, tag exports)
  (3) Python gateway/client scripts and event handlers
  (4) Perspective views, components, bindings, and expressions
  (5) Vision windows, templates, and classic components
  (6) Expression language and transform pipelines
  (7) Named queries and database integrations
  (8) Alarming, historian, and reporting configurations
  Triggers: Ignition, SCADA, Perspective, Vision, tags.json, view.json, system.tag, system.gui, system.perspective, Inductive Automation
---

# Ignition SCADA Developer Skill

Expert guidance for developing Ignition SCADA applications including Perspective views, Vision windows, expressions, bindings, and Python scripting.

## Quick Reference

### Project File Locations
```
project/
├── com.inductiveautomation.perspective/
│   ├── page-config/
│   │   ├── config.json            # Page routing configuration
│   │   └── resource.json
│   ├── session-props/
│   │   ├── props.json             # Session properties
│   │   └── resource.json
│   └── views/
│       └── [ViewName]/
│           ├── view.json          # View structure, root container, components
│           └── resource.json      # View metadata (path, title, permissions)
├── com.inductiveautomation.vision/
│   └── windows/
│       └── [WindowName]/
│           └── window.xml         # Vision window definition
├── ignition/
│   └── script-python/
│       └── [Package]/
│           └── [Module]/
│               ├── code.py        # Project library scripts
│               └── resource.json  # Script resource with hintScope
└── tags/
    └── tags.json                  # Tag provider export
```

**IMPORTANT: Script-python requires DOUBLE nesting!**
- Path: `script-python/MyPackage/MyModule/code.py`
- Call as: `MyPackage.MyModule.functionName()`
- Example: `script-python/SignInBoard/SignInBoard/code.py` → `SignInBoard.SignInBoard.toggleStatus()`

**Script resource.json format:**
```json
{
  "scope": "A",
  "version": 1,
  "restricted": false,
  "overridable": true,
  "files": ["code.py"],
  "attributes": {
    "hintScope": 2,
    "lastModification": {"actor": "admin", "timestamp": "2024-01-01T00:00:00Z"}
  }
}
```

### Key Documentation URLs
When information is needed beyond this skill, search or fetch from:
- **Main Docs**: `https://docs.inductiveautomation.com/`
- **Perspective**: `https://docs.inductiveautomation.com/docs/8.1/perspective`
- **Vision**: `https://docs.inductiveautomation.com/docs/8.1/vision`
- **Scripting**: `https://docs.inductiveautomation.com/docs/8.1/appendix/scripting-functions`
- **Expression Functions**: `https://docs.inductiveautomation.com/docs/8.1/appendix/expression-functions`
- **User Manual**: `https://docs.inductiveautomation.com/docs/8.1/getting-started/user-manual`

## Core Workflows

### 1. Analyzing Existing Projects
When given Ignition project files:
1. Read `resource.json` files to understand view/window hierarchy
2. Parse `view.json` to identify component structure and bindings
3. Extract expression bindings and identify tag references
4. Review Python scripts for event handlers and library functions
5. Cross-reference `tags.json` to understand data model

### 2. Creating Perspective Views
See [references/views.md](references/views.md) for complete patterns.

**Basic view.json structure:**
```json
{
  "custom": {},
  "params": {},
  "root": {
    "type": "ia.container.flex",
    "version": 0,
    "props": {
      "direction": "column",
      "style": { "classes": "" }
    },
    "meta": { "name": "root" },
    "children": []
  }
}
```

**resource.json structure:**
```json
{
  "scope": "G",
  "version": 1,
  "restricted": false,
  "overridable": true,
  "files": ["view.json", "thumbnail.png"],
  "attributes": {
    "lastModification": {
      "actor": "admin",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    "lastModificationSignature": "..."
  }
}
```

### 3. Working with Bindings
See [references/bindings.md](references/bindings.md) for all binding types.

**IMPORTANT: Bindings go in `propConfig`, NOT inline in `props`!**

Correct binding pattern (Designer export format):
```json
{
  "meta": {"name": "MyLabel"},
  "propConfig": {
    "props.text": {
      "binding": {
        "config": {
          "tagPath": "[default]Path/To/Tag"
        },
        "type": "tag"
      }
    },
    "props.style.color": {
      "binding": {
        "config": {
          "expression": "if({[default]Tag/Path} > 100, '#ff0000', '#00ff00')"
        },
        "type": "expr"
      }
    }
  },
  "props": {
    "style": {
      "fontSize": "16px"
    }
  },
  "type": "ia.display.label"
}
```

Note: The old inline binding format (`props.text.binding`) may work but the Designer always exports bindings in `propConfig`.

### 4. Expression Language
See [references/expressions.md](references/expressions.md) for comprehensive reference.

**Expression syntax essentials:**
- Tag references: `{[provider]path/to/tag}`
- Property references: `{this.props.myProp}` or `{view.params.myParam}`
- Conditionals: `if(condition, trueValue, falseValue)`
- Coalesce: `coalesce(value1, value2, default)`
- String formatting: `stringFormat("Value: %s", {tag})`

### 5. Python Scripting
See [references/scripting.md](references/scripting.md) for patterns and system functions.

**Common system functions:**
```python
# Tag operations
system.tag.readBlocking(["[default]Path/To/Tag"])
system.tag.writeBlocking(["[default]Path/To/Tag"], [value])

# Perspective operations
system.perspective.navigate(view="path/to/view", params={"key": "value"})
system.perspective.openPopup(id="popupId", view="path/to/popup")
system.perspective.sendMessage(messageType="myMessage", payload={"data": value})

# Vision operations
system.gui.openWindow("WindowName")
system.nav.swapWindow("FromWindow", "ToWindow")

# Database
system.db.runNamedQuery("QueryPath", {"param": value})
system.db.runPrepQuery("SELECT * FROM table WHERE id = ?", [id])
```

### 6. Tag Configuration
See [references/tags.md](references/tags.md) for tag structure patterns.

**tags.json structure:**
```json
{
  "tags": [
    {
      "name": "FolderName",
      "tagType": "Folder",
      "tags": [
        {
          "name": "MyTag",
          "tagType": "AtomicTag",
          "valueSource": "opc",
          "dataType": "Int4",
          "opcItemPath": "ns=1;s=[PLC]Path.To.Item",
          "engUnit": "gal/min",
          "engLow": 0,
          "engHigh": 100
        }
      ]
    }
  ]
}
```

## Component Reference

### Perspective Components (Common)
| Component | Type String | Key Props |
|-----------|-------------|-----------|
| Flex Container | `ia.container.flex` | direction, wrap, justify, align |
| Column Container | `ia.container.column` | columnCount, gutterSize |
| Coordinate Container | `ia.container.coord` | mode (percent/fixed) |
| Label | `ia.display.label` | text, style |
| Value Display | `ia.display.value-display` | value, format |
| Button | `ia.input.button` | text, enabled, events |
| Numeric Entry | `ia.input.numeric-entry-field` | value, min, max, step |
| Dropdown | `ia.input.dropdown` | options, value, multi |
| Table | `ia.display.table` | data, columns, selection |
| Chart (XY) | `ia.chart.xy` | series, xAxes, yAxes |
| Symbol | `ia.display.symbol` | source, rotation, style |
| Embedded View | `ia.display.view` | path, params |
| Flex Repeater | `ia.display.flex-repeater` | path, instances, direction |

### Vision Components (Common)
| Component | Class | Key Properties |
|-----------|-------|----------------|
| Label | `com.inductiveautomation.factorypmi.application.components.PMILabel` | text, font, foreground |
| Numeric Label | `com.inductiveautomation.factorypmi.application.components.PMINumericLabel` | value, numberFormat |
| Button | `com.inductiveautomation.factorypmi.application.components.PMIButton` | text, enabled |
| Easy Chart | `com.inductiveautomation.factorypmi.application.components.chart.easychart.EasyChart` | tagPens, dateRange |
| Power Table | `com.inductiveautomation.factorypmi.application.components.PMIPowerTable` | data, columnConfig |

## Transforms (Bindings)

Transforms process binding values before application:
```json
{
  "binding": {
    "type": "tag",
    "config": { "tagPath": "[default]Level" },
    "transforms": [
      {
        "type": "expression",
        "expression": "if(value > 80, 'HIGH', if(value < 20, 'LOW', 'NORMAL'))"
      },
      {
        "type": "script",
        "script": "return value.upper()"
      }
    ]
  }
}
```

## Event Handlers

### Perspective Events
```json
{
  "events": {
    "component": {
      "onActionPerformed": {
        "config": {
          "script": "\n\tvalue = self.props.value\n\tsystem.tag.writeBlocking(['[default]Setpoint'], [value])\n"
        },
        "scope": "G",
        "type": "script"
      }
    }
  }
}
```

### Common Event Types
- `onActionPerformed` - Button clicks, form submissions
- `onStartup` / `onShutdown` - View lifecycle
- `onChange` - Value changes
- `onBlur` / `onFocus` - Focus events
- `onMessageReceived` - Message handler

## Best Practices

### View Design
1. Use Flex containers for responsive layouts
2. Implement view params for reusability
3. Use Embedded Views for repeated patterns
4. Define custom properties for internal state
5. Use message handlers for cross-view communication

### Binding Strategy
1. Prefer tag bindings for real-time data
2. Use expression bindings for calculated values
3. Apply transforms for data formatting
4. Use property bindings for component communication
5. Implement bidirectional bindings for input components

### Script Organization
```
Project Scripts/
├── utils/           # General utilities
├── tags/            # Tag operation helpers
├── navigation/      # Navigation functions
├── database/        # Database operations
└── alarms/          # Alarm management
```

### Performance
1. Minimize polling frequency where possible
2. Use indirect tag bindings for dynamic paths
3. Implement pagination for large datasets
4. Cache expensive calculations in view custom properties
5. Use named queries with caching for database reads

## Common Pitfalls (Lessons Learned)

### Project Structure Mistakes
1. **Script-python single nesting**: Scripts MUST be double-nested: `script-python/Package/Module/code.py`
   - Wrong: `script-python/MyScript/code.py`
   - Right: `script-python/MyScript/MyScript/code.py` (called as `MyScript.MyScript.func()`)

2. **Extra resource.json files**: Do NOT create `resource.json` at:
   - `com.inductiveautomation.perspective/resource.json`
   - `com.inductiveautomation.perspective/views/resource.json`
   - `ignition/resource.json`
   - `ignition/script-python/resource.json`
   - Only leaf folders (views, scripts) need resource.json

### View JSON Mistakes
1. **Inline bindings**: Bindings go in `propConfig`, not inline in `props`
   - Wrong: `"props": {"text": {"binding": {...}}}`
   - Right: `"propConfig": {"props.text": {"binding": {...}}}`

2. **Flex Repeater type**: Use `ia.display.flex-repeater` not `ia.container.flexrepeater`

3. **Message handlers format**: Must be an object keyed by message type, not an array

4. **Version field**: Designer may omit `"version": 0` from components - don't require it

### Binding Format
- Tag binding: `{"type": "tag", "config": {"tagPath": "..."}}`
- Expr binding: `{"type": "expr", "config": {"expression": "..."}}`
- Property binding: `{"type": "property", "config": {"path": "view.params.x"}}`

## Troubleshooting

### Common Issues
1. **Binding not updating**: Check tag path syntax, provider name
2. **Expression errors**: Validate function names, parameter types
3. **Script errors**: Check scope (client vs gateway), imports
4. **View not loading**: Verify resource.json integrity, permissions

### Debug Techniques
```python
# Log to console/wrapper log
logger = system.util.getLogger("MyScript")
logger.info("Debug: value = %s" % str(value))

# Perspective console
system.perspective.print("Debug message")
```

## Documentation Lookup

When encountering unfamiliar functions, components, or patterns:

1. **Search Ignition Docs**: Use web_search with query like "Ignition 8.1 [topic]"
2. **Fetch specific pages**: 
   - Scripting: `https://docs.inductiveautomation.com/docs/8.1/appendix/scripting-functions/system-[namespace]`
   - Components: `https://docs.inductiveautomation.com/docs/8.1/perspective/perspective-component-reference`
   - Expression functions: `https://docs.inductiveautomation.com/docs/8.1/appendix/expression-functions`

3. **Inductive Automation Forum**: Search `forum.inductiveautomation.com` for community solutions

Always verify syntax and available functions against the documentation for the specific Ignition version in use.
