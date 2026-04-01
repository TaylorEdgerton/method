# Tag Configuration Reference

## Table of Contents
- [Tag Types](#tag-types)
- [tags.json Structure](#tagsjson-structure)
- [Value Sources](#value-sources)
- [Data Types](#data-types)
- [Tag Properties](#tag-properties)
- [Alarming Configuration](#alarming-configuration)
- [UDT Definitions](#udt-definitions)
- [Common Patterns](#common-patterns)

## Tag Types

| Type | JSON `tagType` | Description |
|------|----------------|-------------|
| Atomic Tag | `AtomicTag` | Single value tag |
| Folder | `Folder` | Container for tags |
| UDT Instance | `UdtInstance` | Instance of a UDT definition |
| UDT Definition | `UdtType` | Template for UDT instances |
| Expression Tag | `AtomicTag` | Tag with expression value source |
| Query Tag | `AtomicTag` | Tag with query value source |
| Derived Tag | `AtomicTag` | Tag derived from other tags |

## tags.json Structure

### Basic Structure
```json
{
  "name": "RootFolder",
  "tagType": "Folder",
  "tags": [
    {
      "name": "SubFolder",
      "tagType": "Folder",
      "tags": []
    },
    {
      "name": "MyTag",
      "tagType": "AtomicTag",
      "valueSource": "memory",
      "dataType": "Int4",
      "value": 0
    }
  ]
}
```

### Export Format (Full tags.json)
```json
{
  "tags": [
    {
      "name": "ProcessArea1",
      "tagType": "Folder",
      "tags": [
        {
          "name": "Tank1",
          "tagType": "Folder",
          "tags": [
            {
              "name": "Level",
              "tagType": "AtomicTag",
              "valueSource": "opc",
              "dataType": "Float4",
              "opcItemPath": "ns=1;s=[PLC1]Tank1.Level",
              "opcServer": "Ignition OPC UA Server",
              "engUnit": "%",
              "engLow": 0.0,
              "engHigh": 100.0,
              "documentation": "Tank 1 level percentage"
            }
          ]
        }
      ]
    }
  ]
}
```

## Value Sources

### Memory
```json
{
  "name": "MemoryTag",
  "tagType": "AtomicTag",
  "valueSource": "memory",
  "dataType": "Int4",
  "value": 0
}
```

### OPC
```json
{
  "name": "OpcTag",
  "tagType": "AtomicTag",
  "valueSource": "opc",
  "dataType": "Float4",
  "opcItemPath": "ns=1;s=[DeviceName]Path.To.Item",
  "opcServer": "Ignition OPC UA Server"
}
```

### Expression
```json
{
  "name": "ExpressionTag",
  "tagType": "AtomicTag",
  "valueSource": "expr",
  "dataType": "Float4",
  "expression": "{[.]../Tag1} + {[.]../Tag2}"
}
```

### Query
```json
{
  "name": "QueryTag",
  "tagType": "AtomicTag",
  "valueSource": "db",
  "dataType": "Int4",
  "queryType": "Select",
  "query": "SELECT value FROM table WHERE id = 1",
  "datasource": "DatabaseName",
  "executionRate": 60000
}
```

### Derived
```json
{
  "name": "DerivedTag",
  "tagType": "AtomicTag",
  "valueSource": "derived",
  "dataType": "Float4",
  "deriveExpressionGetter": "{source} * 1.8 + 32",
  "deriveExpressionSetter": "({value} - 32) / 1.8",
  "sourceTagPath": "[default]Temperature_C"
}
```

### Reference
```json
{
  "name": "ReferenceTag",
  "tagType": "AtomicTag",
  "valueSource": "reference",
  "sourceTagPath": "[default]Path/To/SourceTag"
}
```

## Data Types

| Type | JSON `dataType` | Description |
|------|-----------------|-------------|
| Boolean | `Boolean` | True/False |
| Byte | `Int1` | 8-bit signed integer |
| Short | `Int2` | 16-bit signed integer |
| Integer | `Int4` | 32-bit signed integer |
| Long | `Int8` | 64-bit signed integer |
| Float | `Float4` | 32-bit floating point |
| Double | `Float8` | 64-bit floating point |
| String | `String` | Text value |
| DateTime | `DateTime` | Date and time |
| DataSet | `DataSet` | Tabular data |
| Document | `Document` | JSON document |

## Tag Properties

### Engineering Properties
```json
{
  "engUnit": "gal/min",
  "engLow": 0.0,
  "engHigh": 100.0,
  "engLimitMode": "Clamp",
  "rawLow": 0,
  "rawHigh": 32767,
  "scaledLow": 0.0,
  "scaledHigh": 100.0,
  "scaleMode": "Linear"
}
```

### Documentation
```json
{
  "documentation": "Process temperature sensor",
  "tooltip": "Temperature in degrees F",
  "formatString": "#,##0.0"
}
```

### History Configuration
```json
{
  "historyEnabled": true,
  "historyProvider": "DefaultHistorianProvider",
  "historySampleRate": 1000,
  "historySampleRateUnits": "ms",
  "historyMaxAgeMode": "Days",
  "historyMaxAge": 365,
  "historyTagGroup": "Default Historical",
  "historyTimeDeadband": 0,
  "historyTimeDeadbandUnits": "sec",
  "historyDeadband": 0,
  "historyDeadbandStyle": "Analog",
  "historyDeadbandMode": "Off"
}
```

### Script Events
```json
{
  "eventScripts": [
    {
      "eventid": "valueChanged",
      "script": "\tif currentValue.value > 80:\n\t\tsystem.tag.writeBlocking(['[default]Alarm/HighLevel'], [True])"
    }
  ]
}
```

### Read/Write Permissions
```json
{
  "readPermissions": {
    "type": "AllOf",
    "securityLevels": []
  },
  "writePermissions": {
    "type": "AnyOf",
    "securityLevels": [
      {"name": "Authenticated", "children": []}
    ]
  },
  "readOnly": false
}
```

## Alarming Configuration

### Basic Alarm
```json
{
  "name": "ProcessValue",
  "tagType": "AtomicTag",
  "valueSource": "opc",
  "dataType": "Float4",
  "opcItemPath": "ns=1;s=[PLC]Value",
  "alarms": [
    {
      "name": "HighAlarm",
      "mode": "AboveValue",
      "setpointA": 80.0,
      "priority": "High",
      "displayPath": "Process/HighAlarm",
      "notes": "Value exceeded high limit",
      "label": "Process High Alarm",
      "ackMode": "Auto",
      "enabled": true
    }
  ]
}
```

### Alarm Modes
| Mode | Description | Setpoints |
|------|-------------|-----------|
| `AboveValue` | Triggers above setpoint | `setpointA` |
| `BelowValue` | Triggers below setpoint | `setpointA` |
| `BetweenValues` | Triggers between setpoints | `setpointA`, `setpointB` |
| `OutsideValues` | Triggers outside range | `setpointA`, `setpointB` |
| `OnCondition` | Triggers when true | N/A |
| `EqualValue` | Triggers on specific value | `setpointA` |
| `NotEqualValue` | Triggers when not equal | `setpointA` |
| `AnyChange` | Triggers on any change | N/A |
| `BitState` | Triggers on bit state | `bit`, `bitState` |
| `BadQuality` | Triggers on bad quality | N/A |

### Alarm Priority
- `Diagnostic` (0-249)
- `Low` (250-499)
- `Medium` (500-749)
- `High` (750-999)
- `Critical` (1000)

### Complete Alarm Configuration
```json
{
  "alarms": [
    {
      "name": "HighHigh",
      "mode": "AboveValue",
      "setpointA": 95.0,
      "priority": "Critical",
      "displayPath": "Process/Tank1/LevelAlarms",
      "notes": "Tank level critically high",
      "label": "Tank 1 Level High-High",
      "ackMode": "Manual",
      "enabled": true,
      "activeDelay": 5000,
      "clearDelay": 0,
      "timestampSource": "System",
      "shelvingAllowed": true,
      "deadband": 2.0,
      "deadbandMode": "Constant"
    },
    {
      "name": "High",
      "mode": "AboveValue",
      "setpointA": 80.0,
      "priority": "High"
    },
    {
      "name": "Low",
      "mode": "BelowValue",
      "setpointA": 20.0,
      "priority": "Medium"
    },
    {
      "name": "LowLow",
      "mode": "BelowValue",
      "setpointA": 5.0,
      "priority": "High"
    }
  ]
}
```

## UDT Definitions

### UDT Definition
```json
{
  "name": "Motor",
  "tagType": "UdtType",
  "tags": [
    {
      "name": "Running",
      "tagType": "AtomicTag",
      "valueSource": "opc",
      "dataType": "Boolean",
      "opcItemPath": "ns=1;s=[{PLCName}]{BasePath}.Running"
    },
    {
      "name": "Speed",
      "tagType": "AtomicTag",
      "valueSource": "opc",
      "dataType": "Float4",
      "opcItemPath": "ns=1;s=[{PLCName}]{BasePath}.Speed",
      "engUnit": "RPM",
      "engLow": 0,
      "engHigh": 1800
    },
    {
      "name": "Runtime",
      "tagType": "AtomicTag",
      "valueSource": "expr",
      "dataType": "Float4",
      "expression": "if({[.]Running}, secondsBetween({[.]LastStart}, now(1000))/3600, 0)"
    }
  ],
  "parameters": {
    "PLCName": {
      "dataType": "String",
      "value": "PLC1"
    },
    "BasePath": {
      "dataType": "String",
      "value": "Motor1"
    }
  }
}
```

### UDT Instance
```json
{
  "name": "Pump1_Motor",
  "tagType": "UdtInstance",
  "typeId": "Motor",
  "parameters": {
    "PLCName": "PLC1",
    "BasePath": "Pump1"
  }
}
```

### Nested UDT
```json
{
  "name": "Pump",
  "tagType": "UdtType",
  "tags": [
    {
      "name": "Motor",
      "tagType": "UdtInstance",
      "typeId": "Motor",
      "parameters": {
        "PLCName": "{PLCName}",
        "BasePath": "{BasePath}.Motor"
      }
    },
    {
      "name": "Discharge_Pressure",
      "tagType": "AtomicTag",
      "valueSource": "opc",
      "dataType": "Float4",
      "opcItemPath": "ns=1;s=[{PLCName}]{BasePath}.DischargePSI"
    }
  ],
  "parameters": {
    "PLCName": {"dataType": "String", "value": ""},
    "BasePath": {"dataType": "String", "value": ""}
  }
}
```

## Common Patterns

### Folder with Standard Tags
```json
{
  "name": "ProcessArea",
  "tagType": "Folder",
  "tags": [
    {
      "name": "_Meta",
      "tagType": "Folder",
      "tags": [
        {"name": "Description", "tagType": "AtomicTag", "valueSource": "memory", "dataType": "String", "value": "Process Area 1"},
        {"name": "LastModified", "tagType": "AtomicTag", "valueSource": "memory", "dataType": "DateTime"}
      ]
    },
    {
      "name": "Setpoints",
      "tagType": "Folder",
      "tags": []
    },
    {
      "name": "ProcessValues",
      "tagType": "Folder",
      "tags": []
    },
    {
      "name": "Alarms",
      "tagType": "Folder",
      "tags": []
    }
  ]
}
```

### Calculated Status Tag
```json
{
  "name": "SystemStatus",
  "tagType": "AtomicTag",
  "valueSource": "expr",
  "dataType": "Int4",
  "expression": "if({[.]Fault}, 3, if({[.]Running}, 1, if({[.]Ready}, 2, 0)))"
}
```

### Rollup Tag (Any True)
```json
{
  "name": "AnyAlarmActive",
  "tagType": "AtomicTag",
  "valueSource": "expr",
  "dataType": "Boolean",
  "expression": "{[.]Device1/Alarm} || {[.]Device2/Alarm} || {[.]Device3/Alarm}"
}
```

### Counter Tag with Reset
```json
{
  "name": "ProductionCount",
  "tagType": "AtomicTag",
  "valueSource": "opc",
  "dataType": "Int4",
  "opcItemPath": "ns=1;s=[PLC]Counter",
  "eventScripts": [
    {
      "eventid": "valueChanged",
      "script": "\t# Reset daily at midnight\n\timport datetime\n\tnow = datetime.datetime.now()\n\tif now.hour == 0 and now.minute == 0:\n\t\tsystem.tag.writeBlocking(['[default]DailyCount'], [0])"
    }
  ]
}
```

### Tag Path Reference Patterns
```
{[.]SiblingTag}              # Same folder
{[.]../ParentFolderTag}      # Parent folder
{[.]../../GrandparentTag}    # Two levels up
{[.]Subfolder/ChildTag}      # Child folder
{[default]Absolute/Path}     # Absolute path
{[{ProviderParam}]Path}      # Parameterized provider
{[.]{PathParam}/Tag}         # Parameterized path
```
