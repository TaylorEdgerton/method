# Bindings Reference

## Table of Contents
- [Binding Types](#binding-types)
- [Tag Bindings](#tag-bindings)
- [Expression Bindings](#expression-bindings)
- [Property Bindings](#property-bindings)
- [Query Bindings](#query-bindings)
- [Indirect Bindings](#indirect-bindings)
- [Transforms](#transforms)
- [Bidirectional Bindings](#bidirectional-bindings)
- [JSON Structure Patterns](#json-structure-patterns)

## Binding Types

| Type | JSON `type` | Use Case |
|------|-------------|----------|
| Tag | `tag` | Direct tag value subscription |
| Expression | `expr` | Calculated values, conditionals |
| Property | `property` | Reference other properties |
| Query | `query` | Named query results |
| Indirect Tag | `tag` with indirect | Dynamic tag paths |
| Function | `function` | Transform pipelines |

## Tag Bindings

### Basic Tag Binding
```json
{
  "props": {
    "value": {
      "binding": {
        "type": "tag",
        "config": {
          "tagPath": "[default]Path/To/Tag"
        }
      }
    }
  }
}
```

### Tag with Fallback
```json
{
  "binding": {
    "type": "tag",
    "config": {
      "tagPath": "[default]Path/To/Tag",
      "fallbackValue": 0
    }
  }
}
```

### Tag Providers
```
[default]           # Default tag provider
[System]            # System tags
[client]            # Client tags (Vision)
[gateway]           # Gateway scoped tags
[custom_provider]   # Custom OPC/DB providers
```

### Tag Properties
```json
{
  "binding": {
    "type": "tag",
    "config": {
      "tagPath": "[default]Tag.engHigh"
    }
  }
}
```
Properties: `value`, `quality`, `timestamp`, `engHigh`, `engLow`, `engUnit`, `tooltip`, `documentation`

## Expression Bindings

### Basic Expression
```json
{
  "binding": {
    "type": "expr",
    "config": {
      "expression": "if({[default]Value} > 100, 'High', 'Normal')"
    }
  }
}
```

### Multi-line Expression
```json
{
  "binding": {
    "type": "expr",
    "config": {
      "expression": "if({[default]Status} = 0, 'Stopped',\n  if({[default]Status} = 1, 'Running',\n    if({[default]Status} = 2, 'Fault', 'Unknown')))"
    }
  }
}
```

### Expression with Property References
```json
{
  "binding": {
    "type": "expr",
    "config": {
      "expression": "stringFormat('%s: %.1f %s', \n  {this.props.label},\n  {[default]Process/Value},\n  {view.params.unit})"
    }
  }
}
```

## Property Bindings

### Same Component Property
```json
{
  "binding": {
    "type": "property",
    "config": {
      "path": "this.props.value"
    }
  }
}
```

### View Parameter
```json
{
  "binding": {
    "type": "property",
    "config": {
      "path": "view.params.deviceId"
    }
  }
}
```

### View Custom Property
```json
{
  "binding": {
    "type": "property",
    "config": {
      "path": "view.custom.selectedItem"
    }
  }
}
```

### Session Property
```json
{
  "binding": {
    "type": "property",
    "config": {
      "path": "session.props.user.username"
    }
  }
}
```

### Page Property
```json
{
  "binding": {
    "type": "property",
    "config": {
      "path": "page.props.id"
    }
  }
}
```

## Query Bindings

### Named Query
```json
{
  "binding": {
    "type": "query",
    "config": {
      "queryPath": "Reports/GetProductionData",
      "parameters": {
        "startDate": "{view.params.startDate}",
        "endDate": "{view.params.endDate}",
        "lineId": "{view.params.lineId}"
      },
      "polling": {
        "enabled": true,
        "rate": 5000
      }
    }
  }
}
```

### Query with Caching
```json
{
  "binding": {
    "type": "query",
    "config": {
      "queryPath": "Lookup/GetAreaList",
      "parameters": {},
      "caching": {
        "enabled": true,
        "scope": "session"
      }
    }
  }
}
```

## Indirect Bindings

### Dynamic Tag Path
```json
{
  "binding": {
    "type": "tag",
    "config": {
      "mode": "indirect",
      "tagPath": "[default]{view.params.devicePath}/Temperature",
      "fallbackValue": null
    }
  }
}
```

### Indirect with Expression Path
```json
{
  "binding": {
    "type": "tag",
    "config": {
      "mode": "indirect",
      "tagPath": "[default]Line{this.custom.selectedLine}/Speed"
    }
  }
}
```

### Fully Dynamic Path
```json
{
  "binding": {
    "type": "tag",
    "config": {
      "mode": "indirect",
      "tagPath": "{view.custom.fullTagPath}"
    }
  }
}
```

## Transforms

Transforms process binding results sequentially.

### Expression Transform
```json
{
  "binding": {
    "type": "tag",
    "config": {
      "tagPath": "[default]RawValue"
    },
    "transforms": [
      {
        "type": "expression",
        "expression": "value * {view.params.scaleFactor}"
      }
    ]
  }
}
```

### Script Transform
```json
{
  "transforms": [
    {
      "type": "script",
      "script": "\tif value is None:\n\t\treturn 'N/A'\n\treturn '{:.2f}'.format(value)"
    }
  ]
}
```

### Map Transform
```json
{
  "transforms": [
    {
      "type": "map",
      "inputType": "value",
      "outputType": "value",
      "mappings": [
        {"input": 0, "output": "Stopped"},
        {"input": 1, "output": "Running"},
        {"input": 2, "output": "Fault"}
      ],
      "fallback": "Unknown"
    }
  ]
}
```

### Format Transform
```json
{
  "transforms": [
    {
      "type": "format",
      "format": "#,##0.00",
      "locale": "en-US"
    }
  ]
}
```

### Object Transform (Extract Property)
```json
{
  "transforms": [
    {
      "type": "object",
      "config": {
        "property": "rows[0].value"
      }
    }
  ]
}
```

### Chained Transforms
```json
{
  "transforms": [
    {
      "type": "expression",
      "expression": "value * 100"
    },
    {
      "type": "format",
      "format": "0.0"
    },
    {
      "type": "expression",
      "expression": "value + '%'"
    }
  ]
}
```

## Bidirectional Bindings

For input components that need to write back to tags.

### Numeric Input
```json
{
  "props": {
    "value": {
      "binding": {
        "type": "tag",
        "config": {
          "tagPath": "[default]Setpoint",
          "bidirectional": true
        }
      }
    }
  }
}
```

### Bidirectional Expression (Read/Write Different Tags)
```json
{
  "props": {
    "value": {
      "binding": {
        "type": "tag",
        "config": {
          "tagPath": "[default]Feedback",
          "bidirectional": {
            "enabled": true,
            "targetPath": "[default]Setpoint"
          }
        }
      }
    }
  }
}
```

## JSON Structure Patterns

### Complete Component with Bindings
```json
{
  "type": "ia.display.label",
  "version": 0,
  "props": {
    "text": {
      "binding": {
        "type": "expr",
        "config": {
          "expression": "stringFormat('%.1f°F', {[default]Temperature})"
        }
      }
    },
    "style": {
      "classes": "status-label",
      "color": {
        "binding": {
          "type": "expr",
          "config": {
            "expression": "if({[default]Temperature} > 100, 'var(--error)', 'var(--success)')"
          }
        }
      }
    }
  },
  "meta": {
    "name": "TemperatureLabel"
  }
}
```

### Binding in Nested Property
```json
{
  "props": {
    "columns": [
      {
        "field": "status",
        "header": "Status",
        "render": {
          "binding": {
            "type": "property",
            "config": {
              "path": "this.props.columns[0].renderConfig"
            }
          }
        }
      }
    ]
  }
}
```

### Array Item Bindings
```json
{
  "props": {
    "options": {
      "binding": {
        "type": "query",
        "config": {
          "queryPath": "Lookups/GetOptions"
        },
        "transforms": [
          {
            "type": "script",
            "script": "\treturn [{'label': row['name'], 'value': row['id']} for row in value]"
          }
        ]
      }
    }
  }
}
```

### Conditional Binding Enable
Use view custom properties or scripting to conditionally fetch data:
```json
{
  "binding": {
    "type": "query",
    "config": {
      "queryPath": "Reports/GetData",
      "enabled": {
        "binding": {
          "type": "property",
          "config": {
            "path": "view.custom.dataEnabled"
          }
        }
      }
    }
  }
}
```
