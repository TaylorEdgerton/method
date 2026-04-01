# Perspective Views Reference

## Table of Contents
- [View Structure](#view-structure)
- [Container Types](#container-types)
- [Component Structure](#component-structure)
- [View Parameters](#view-parameters)
- [Custom Properties](#custom-properties)
- [Events and Actions](#events-and-actions)
- [Styles and Classes](#styles-and-classes)
- [Embedded Views](#embedded-views)
- [Common Patterns](#common-patterns)

## View Structure

### view.json
```json
{
  "custom": {
    "selectedId": null,
    "isLoading": false
  },
  "params": {
    "deviceId": "string",
    "startDate": "date"
  },
  "root": {
    "type": "ia.container.flex",
    "version": 0,
    "props": {},
    "meta": {"name": "root"},
    "children": []
  }
}
```

### resource.json
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
    }
  }
}
```

Scope values: `"G"` (Gateway), `"D"` (Designer), `"C"` (Client), `"A"` (All)

## Container Types

### Flex Container
```json
{
  "type": "ia.container.flex",
  "props": {
    "direction": "column",
    "wrap": "nowrap",
    "justify": "flex-start",
    "alignItems": "stretch",
    "alignContent": "flex-start",
    "style": {
      "gap": "10px",
      "padding": "10px"
    }
  },
  "children": []
}
```

Direction: `"row"`, `"column"`, `"row-reverse"`, `"column-reverse"`
Justify: `"flex-start"`, `"flex-end"`, `"center"`, `"space-between"`, `"space-around"`, `"space-evenly"`
Align: `"flex-start"`, `"flex-end"`, `"center"`, `"stretch"`, `"baseline"`

### Column Container
```json
{
  "type": "ia.container.column",
  "props": {
    "columnCount": 3,
    "gutterSize": 10,
    "style": {}
  },
  "children": []
}
```

### Coordinate Container
```json
{
  "type": "ia.container.coord",
  "props": {
    "mode": "percent",
    "style": {
      "overflow": "hidden"
    }
  },
  "children": [
    {
      "type": "ia.display.label",
      "position": {
        "x": 10,
        "y": 10,
        "width": 100,
        "height": 30
      },
      "props": {"text": "Label"}
    }
  ]
}
```

Mode: `"percent"` (0-100), `"fixed"` (pixels)

### Tab Container
```json
{
  "type": "ia.container.tab",
  "props": {
    "selectedTab": 0,
    "tabPosition": "top",
    "tabs": [
      {"label": "Overview", "icon": "material/dashboard"},
      {"label": "Details", "icon": "material/info"}
    ]
  },
  "children": [
    {"type": "ia.container.flex", "props": {}},
    {"type": "ia.container.flex", "props": {}}
  ]
}
```

### Split Container
```json
{
  "type": "ia.container.split",
  "props": {
    "orientation": "horizontal",
    "position": 30,
    "collapseThreshold": 5
  },
  "children": [
    {"type": "ia.container.flex", "props": {}, "meta": {"name": "left"}},
    {"type": "ia.container.flex", "props": {}, "meta": {"name": "right"}}
  ]
}
```

## Component Structure

### Basic Component
```json
{
  "type": "ia.display.label",
  "version": 0,
  "props": {
    "text": "Hello World",
    "style": {
      "fontSize": "16px",
      "fontWeight": "bold",
      "color": "var(--neutral-80)"
    }
  },
  "meta": {
    "name": "myLabel"
  },
  "position": {},
  "custom": {},
  "events": {}
}
```

### With Binding (Correct propConfig Format)

**IMPORTANT: Bindings go in `propConfig`, NOT inline in `props`!**

```json
{
  "meta": {"name": "valueDisplay"},
  "propConfig": {
    "props.value": {
      "binding": {
        "config": {"tagPath": "[default]Value"},
        "type": "tag"
      }
    }
  },
  "props": {
    "format": {
      "format": "0.00"
    }
  },
  "type": "ia.display.value-display"
}
```

Multiple bindings example:
```json
{
  "meta": {"name": "statusIcon"},
  "propConfig": {
    "props.path": {
      "binding": {
        "config": {"expression": "if({view.params.isIn}, 'material/check', 'material/close')"},
        "type": "expr"
      }
    },
    "props.style.color": {
      "binding": {
        "config": {"expression": "if({view.params.isIn}, '#4caf50', '#9e9e9e')"},
        "type": "expr"
      }
    }
  },
  "props": {
    "style": {"fontSize": "24px"}
  },
  "type": "ia.display.icon"
}
```

## View Parameters

### Parameter Definition
```json
{
  "params": {
    "deviceId": {
      "paramType": "value",
      "valueType": "string",
      "defaultValue": ""
    },
    "startDate": {
      "paramType": "value",
      "valueType": "date",
      "defaultValue": null
    },
    "showDetails": {
      "paramType": "value",
      "valueType": "boolean", 
      "defaultValue": true
    }
  }
}
```

### Simple Parameter Declaration (Common)
```json
{
  "params": {
    "deviceId": "",
    "lineNumber": 1,
    "mode": "auto"
  }
}
```

### Using Parameters in Bindings
```json
{
  "binding": {
    "type": "tag",
    "config": {
      "mode": "indirect",
      "tagPath": "[default]Devices/{view.params.deviceId}/Status"
    }
  }
}
```

## Custom Properties

### View-Level Custom Properties
```json
{
  "custom": {
    "selectedRow": null,
    "filterText": "",
    "refreshTrigger": 0,
    "calculatedValue": {
      "binding": {
        "type": "expr",
        "config": {
          "expression": "{[default]Value1} + {[default]Value2}"
        }
      }
    }
  }
}
```

### Component-Level Custom Properties
```json
{
  "type": "ia.container.flex",
  "custom": {
    "isExpanded": false,
    "itemCount": 0
  },
  "props": {}
}
```

### Accessing Custom Properties
- View custom: `{view.custom.propertyName}`
- Component custom: `{this.custom.propertyName}`

## Events and Actions

### Script Event Handler
```json
{
  "events": {
    "component": {
      "onActionPerformed": {
        "type": "script",
        "scope": "G",
        "config": {
          "script": "\tvalue = self.props.value\n\tsystem.tag.writeBlocking(['[default]Setpoint'], [value])"
        }
      }
    }
  }
}
```

### Navigation Action
```json
{
  "events": {
    "component": {
      "onActionPerformed": {
        "type": "navigation",
        "config": {
          "target": "tab",
          "url": "/perspective/main/details",
          "params": {
            "id": "{this.custom.selectedId}"
          }
        }
      }
    }
  }
}
```

### Popup Action
```json
{
  "events": {
    "component": {
      "onActionPerformed": {
        "type": "popup",
        "config": {
          "id": "detailPopup",
          "view": "Popups/DetailView",
          "params": {
            "itemId": "{view.custom.selectedId}"
          },
          "modal": true,
          "draggable": true,
          "position": {
            "left": "50%",
            "top": "50%"
          }
        }
      }
    }
  }
}
```

### Send Message Action
```json
{
  "events": {
    "component": {
      "onActionPerformed": {
        "type": "sendMessage",
        "config": {
          "messageType": "refreshData",
          "payload": {
            "source": "button"
          },
          "scope": "view"
        }
      }
    }
  }
}
```

### Message Handler (View Level)
```json
{
  "events": {
    "messageHandlers": [
      {
        "messageType": "refreshData",
        "script": "\tself.custom.refreshTrigger = self.custom.refreshTrigger + 1"
      }
    ]
  }
}
```

### Common Event Types
- `onStartup` - View/component initialization
- `onShutdown` - View/component cleanup
- `onActionPerformed` - Button click, form submit
- `onChange` - Value changed
- `onBlur` - Lost focus
- `onFocus` - Gained focus
- `onRowClick` - Table row clicked
- `onSelectionChange` - Selection changed

## Styles and Classes

### Inline Styles
```json
{
  "props": {
    "style": {
      "backgroundColor": "#ffffff",
      "border": "1px solid #ccc",
      "borderRadius": "4px",
      "padding": "10px",
      "margin": "5px"
    }
  }
}
```

### CSS Classes
```json
{
  "props": {
    "style": {
      "classes": "my-custom-class another-class"
    }
  }
}
```

### Dynamic Styles with Binding
```json
{
  "props": {
    "style": {
      "backgroundColor": {
        "binding": {
          "type": "expr",
          "config": {
            "expression": "if({[default]Alarm}, 'var(--error)', 'var(--success)')"
          }
        }
      }
    }
  }
}
```

### Theme Variables
```
var(--neutral-10) through var(--neutral-100)
var(--primary)
var(--secondary) 
var(--warning)
var(--error)
var(--success)
var(--info)
```

## Embedded Views

### Basic Embedded View
```json
{
  "type": "ia.display.view",
  "props": {
    "path": "Components/StatusIndicator",
    "params": {
      "tagPath": "[default]Device1/Status",
      "label": "Device 1"
    },
    "useDefaultWidth": true,
    "useDefaultHeight": true
  },
  "meta": {"name": "statusView"}
}
```

### Dynamic View Path
```json
{
  "type": "ia.display.view",
  "props": {
    "path": {
      "binding": {
        "type": "expr",
        "config": {
          "expression": "'Templates/' + {view.params.templateType}"
        }
      }
    },
    "params": {
      "deviceId": "{view.params.deviceId}"
    }
  }
}
```

### Flex Repeater (Array of Views)

**IMPORTANT: Type is `ia.display.flex-repeater` (NOT `ia.container.flex-repeater`)**

```json
{
  "meta": {"name": "MyRepeater"},
  "props": {
    "direction": "column",
    "path": "Components/ItemCard",
    "useDefaultViewHeight": true,
    "useDefaultViewWidth": true,
    "instances": [
      {
        "instancePosition": {},
        "instanceStyle": {"classes": ""},
        "itemId": "123",
        "name": "First Item"
      },
      {
        "instancePosition": {},
        "instanceStyle": {"classes": ""},
        "itemId": "456",
        "name": "Second Item"
      }
    ]
  },
  "type": "ia.display.flex-repeater"
}
```

**Instances format:**
- Each instance object contains `instancePosition`, `instanceStyle`, plus any view params
- The view params (e.g., `itemId`, `name`) are passed directly to the embedded view
- The embedded view should have matching params defined

**With binding (in propConfig):**
```json
{
  "meta": {"name": "PeopleRepeater"},
  "propConfig": {
    "props.instances": {
      "binding": {
        "config": {
          "tagPath": "[default]Office/SignInBoard/People"
        },
        "transforms": [
          {
            "code": "# Transform tag browse results to instances\npeople = []\nbrowseResults = system.tag.browse('[default]People')\nfor result in browseResults.getResults():\n\tpeople.append({\n\t\t'instancePosition': {},\n\t\t'instanceStyle': {'classes': ''},\n\t\t'personId': result['name'],\n\t\t'displayName': result['name']\n\t})\nreturn people",
            "type": "script"
          }
        ],
        "type": "tag"
      }
    }
  },
  "props": {
    "direction": "column",
    "path": "Views/PersonRow"
  },
  "type": "ia.display.flex-repeater"
}
```

## Common Patterns

### Master-Detail Layout
```json
{
  "type": "ia.container.split",
  "props": {"orientation": "horizontal", "position": 30},
  "children": [
    {
      "type": "ia.display.table",
      "props": {
        "data": {"binding": {"type": "query", "config": {"queryPath": "GetItems"}}},
        "selection": {"enabled": true, "mode": "single"}
      },
      "events": {
        "component": {
          "onSelectionChange": {
            "type": "script",
            "config": {
              "script": "\tselected = self.props.selection.selectedRow\n\tif selected:\n\t\tself.getSibling('detailView').props.params = {'id': selected['id']}"
            }
          }
        }
      }
    },
    {
      "type": "ia.display.view",
      "meta": {"name": "detailView"},
      "props": {
        "path": "Details/ItemDetail",
        "params": {"id": null}
      }
    }
  ]
}
```

### Loading State Pattern
```json
{
  "custom": {
    "isLoading": true,
    "data": {
      "binding": {
        "type": "query",
        "config": {"queryPath": "GetData"},
        "transforms": [
          {
            "type": "script",
            "script": "\tself.custom.isLoading = False\n\treturn value"
          }
        ]
      }
    }
  },
  "root": {
    "type": "ia.container.flex",
    "children": [
      {
        "type": "ia.display.spinner",
        "props": {
          "visible": {"binding": {"type": "property", "config": {"path": "view.custom.isLoading"}}}
        }
      }
    ]
  }
}
```

### Form with Validation
```json
{
  "custom": {
    "formData": {
      "name": "",
      "value": 0
    },
    "errors": {}
  },
  "root": {
    "children": [
      {
        "type": "ia.input.text-field",
        "props": {
          "value": {"binding": {"type": "property", "config": {"path": "view.custom.formData.name"}, "bidirectional": true}}
        }
      },
      {
        "type": "ia.input.button",
        "props": {"text": "Submit"},
        "events": {
          "component": {
            "onActionPerformed": {
              "type": "script",
              "config": {
                "script": "\tdata = self.view.custom.formData\n\tif not data['name']:\n\t\tself.view.custom.errors = {'name': 'Required'}\n\t\treturn\n\t# Submit logic here"
              }
            }
          }
        }
      }
    ]
  }
}
```
