# Python Scripting Reference

## Table of Contents
- [Scripting Contexts](#scripting-contexts)
- [System Functions](#system-functions)
- [Tag Operations](#tag-operations)
- [Database Operations](#database-operations)
- [Perspective Functions](#perspective-functions)
- [Vision Functions](#vision-functions)
- [Utility Functions](#utility-functions)
- [Alarming](#alarming)
- [Common Patterns](#common-patterns)
- [Script Libraries](#script-libraries)

## Scripting Contexts

### Gateway Scope
- Runs on the Ignition Gateway server
- Access to all tags, database, services
- Cannot access client GUI functions
- Used in: Gateway event scripts, tag event scripts, named query scripts

### Client Scope (Perspective)
- Runs in browser session context
- Access to session, page, view objects
- Uses `system.perspective.*` functions
- Used in: Component events, view events, message handlers

### Client Scope (Vision)
- Runs in Vision client JVM
- Access to window, component objects
- Uses `system.gui.*`, `system.nav.*` functions
- Used in: Component events, window scripts

## System Functions

### system.tag - Tag Operations
```python
# Read single tag
value = system.tag.readBlocking(["[default]Path/To/Tag"])[0].value

# Read multiple tags
results = system.tag.readBlocking([
    "[default]Tag1",
    "[default]Tag2",
    "[default]Tag3"
])
for qv in results:
    print(qv.value, qv.quality)

# Write single tag
system.tag.writeBlocking(["[default]Path/To/Tag"], [newValue])

# Write multiple tags
system.tag.writeBlocking(
    ["[default]Tag1", "[default]Tag2"],
    [value1, value2]
)

# Async write (non-blocking)
system.tag.writeAsync(["[default]Tag"], [value])

# Browse tags
tags = system.tag.browse("[default]FolderPath")
for tag in tags:
    print(tag["name"], tag["tagType"])

# Check if tag exists
exists = system.tag.exists("[default]Path/To/Tag")

# Read tag property
config = system.tag.readBlocking(["[default]Tag.engHigh"])[0].value

# Configure tag (create/modify)
config = {
    "name": "NewTag",
    "tagType": "AtomicTag",
    "valueSource": "memory",
    "dataType": "Float8"
}
system.tag.configure("[default]FolderPath", [config])
```

### system.db - Database Operations
```python
# Run named query
results = system.db.runNamedQuery("QueryPath", {"param1": value1})

# Run named query with project
results = system.db.runNamedQuery("ProjectName", "QueryPath", {"param1": value1})

# Run prepared query
results = system.db.runPrepQuery(
    "SELECT * FROM table WHERE id = ?",
    [id],
    "DatabaseName"
)

# Run update query
rowsAffected = system.db.runPrepUpdate(
    "UPDATE table SET value = ? WHERE id = ?",
    [newValue, id],
    "DatabaseName"
)

# Run scalar query
count = system.db.runScalarQuery("SELECT COUNT(*) FROM table", "DatabaseName")

# Transaction
tx = system.db.beginTransaction("DatabaseName", timeout=30000)
try:
    system.db.runPrepUpdate("UPDATE ...", [], tx=tx)
    system.db.runPrepUpdate("INSERT ...", [], tx=tx)
    system.db.commitTransaction(tx)
except:
    system.db.rollbackTransaction(tx)
    raise
finally:
    system.db.closeTransaction(tx)

# Dataset operations
dataset = system.db.runNamedQuery("GetData", {})
for row in range(dataset.rowCount):
    col1 = dataset.getValueAt(row, "columnName")
    col2 = dataset.getValueAt(row, 1)  # By index

# Convert to Python list
data = system.dataset.toPyDataSet(dataset)
for row in data:
    print(row["columnName"])
```

## Perspective Functions

### Navigation
```python
# Navigate to view
system.perspective.navigate(view="Path/To/View")

# Navigate with params
system.perspective.navigate(
    view="Path/To/View",
    params={"id": 123, "mode": "edit"}
)

# Navigate in specific page
system.perspective.navigate(
    view="Path/To/View",
    page="MainPage"
)

# Open URL
system.perspective.openUrl("https://example.com", target="_blank")
```

### Popups
```python
# Open popup
system.perspective.openPopup(
    id="myPopup",
    view="Popups/DetailView",
    params={"itemId": 123},
    modal=True,
    draggable=True,
    resizable=True,
    position={"left": "50%", "top": "50%"},
    showCloseIcon=True
)

# Close popup
system.perspective.closePopup("myPopup")
```

### Docking
```python
# Open dock
system.perspective.openDock(
    id="sideDock",
    view="Docks/Navigation",
    position="left",
    size=300
)

# Close dock
system.perspective.closeDock("sideDock")

# Toggle dock
system.perspective.toggleDock("sideDock")
```

### Messaging
```python
# Send message to view
system.perspective.sendMessage(
    messageType="refreshData",
    payload={"source": "button"},
    scope="view"
)

# Send to page
system.perspective.sendMessage(
    messageType="updateStatus",
    payload={"status": "complete"},
    scope="page"
)

# Send to session
system.perspective.sendMessage(
    messageType="notification",
    payload={"message": "Task complete"},
    scope="session"
)
```

### Session Operations
```python
# Get session info
session = system.perspective.getSessionInfo()
username = session["auth"]["user"]["userName"]

# Print to browser console
system.perspective.print("Debug: " + str(value))

# Download file
system.perspective.download(
    filename="report.csv",
    data=csvContent,
    contentType="text/csv"
)

# Alter logging
system.perspective.alterLogging(
    remoteLoggingEnabled=True,
    level="debug"
)
```

## Vision Functions

### Window Operations
```python
# Open window
system.gui.openWindow("WindowName")

# Open with params
system.gui.openWindow("WindowName", {"param": value})

# Close window
system.gui.closeWindow("WindowName")

# Get window reference
window = system.gui.getWindow("WindowName")
window.rootContainer.getComponent("ComponentName").text = "New Value"

# Navigate (swap windows)
system.nav.swapWindow("OldWindow", "NewWindow")

# Open popup
window = system.gui.openWindow("PopupWindow")
system.nav.centerWindow("PopupWindow")
```

### Component Access
```python
# Get component in event script
component = event.source

# Get sibling component
sibling = event.source.parent.getComponent("SiblingName")

# Get root container
root = system.gui.getParentWindow(event).rootContainer

# Get component by path
comp = root.getComponent("Container/SubContainer/MyComponent")

# Modify properties
component.text = "New Text"
component.enabled = False
component.visible = True
```

### Dialogs
```python
# Message box
system.gui.messageBox("Message", "Title")

# Confirmation
result = system.gui.confirm("Are you sure?", "Confirm")
if result:
    # User clicked Yes
    pass

# Input dialog
value = system.gui.inputBox("Enter value:", "Input")

# Error box
system.gui.errorBox("Error message", "Error")

# Warning box
system.gui.warningBox("Warning message", "Warning")
```

## Utility Functions

### system.util
```python
# Get logger
logger = system.util.getLogger("MyScript")
logger.info("Information message")
logger.warn("Warning message")
logger.error("Error message")
logger.debug("Debug message")

# JSON operations
jsonString = system.util.jsonEncode(pythonDict)
pythonObj = system.util.jsonDecode(jsonString)

# Sleep (use sparingly)
system.util.sleep(1000)  # milliseconds

# Get system time
now = system.date.now()

# Execute in background (Gateway)
def backgroundTask():
    # Long running operation
    pass
system.util.invokeAsynchronous(backgroundTask)

# Invoke later (Vision client)
def updateUI():
    component.text = "Updated"
system.util.invokeLater(updateUI)

# Get project name
project = system.util.getProjectName()

# Get gateway address
gateway = system.util.getGatewayAddress()
```

### system.date
```python
# Current time
now = system.date.now()

# Format date
formatted = system.date.format(now, "yyyy-MM-dd HH:mm:ss")

# Parse date
parsed = system.date.parse("2024-01-15", "yyyy-MM-dd")

# Add time
tomorrow = system.date.addDays(now, 1)
nextHour = system.date.addHours(now, 1)
nextWeek = system.date.addWeeks(now, 1)

# Get components
year = system.date.getYear(now)
month = system.date.getMonth(now)
day = system.date.getDayOfMonth(now)
hour = system.date.getHour24(now)

# Date arithmetic
diff = system.date.secondsBetween(startDate, endDate)
diff = system.date.minutesBetween(startDate, endDate)
diff = system.date.hoursBetween(startDate, endDate)
diff = system.date.daysBetween(startDate, endDate)

# Start/end of day
startOfDay = system.date.midnight(now)
startOfMonth = system.date.getDate(year, month, 1)
```

### system.dataset
```python
# Create dataset
headers = ["id", "name", "value"]
data = [
    [1, "Item 1", 100],
    [2, "Item 2", 200]
]
dataset = system.dataset.toDataSet(headers, data)

# Add row
newDataset = system.dataset.addRow(dataset, [3, "Item 3", 300])

# Delete row
newDataset = system.dataset.deleteRow(dataset, rowIndex)

# Update value
newDataset = system.dataset.setValue(dataset, rowIndex, "value", 150)

# Get column as list
values = system.dataset.getColumnAsList(dataset, "value")

# Filter dataset
filtered = system.dataset.filterData(dataset, {"name": "Item 1"})

# Sort dataset
sorted = system.dataset.sort(dataset, "name", True)  # ascending

# Convert to/from Python
pyData = system.dataset.toPyDataSet(dataset)
dataset = system.dataset.toDataSet(headers, list(pyData))

# Export to CSV
csvString = system.dataset.toCSV(dataset)
```

## Alarming

```python
# Get active alarms
alarms = system.alarm.queryStatus(
    source=["*"],
    state=["ActiveUnacked", "ActiveAcked"]
)

# Acknowledge alarms
system.alarm.acknowledge(
    source=["[default]Path/To/*"],
    state=["ActiveUnacked"]
)

# Shelve alarm
system.alarm.shelve(
    source=["[default]MyAlarm"],
    shelveDuration=3600000  # 1 hour in ms
)

# Query alarm journal
history = system.alarm.queryJournal(
    startDate=system.date.addDays(system.date.now(), -7),
    endDate=system.date.now(),
    source=["*"],
    includeShelved=True
)
```

## Common Patterns

### Event Script Template
```python
# Button click handler
def onClick(event):
    try:
        # Get component reference
        button = event.source
        
        # Get view/window custom properties
        # Perspective:
        viewCustom = self.view.custom
        # Vision:
        rootContainer = event.source.parent
        
        # Perform operation
        value = button.custom.targetValue
        tagPath = button.custom.tagPath
        system.tag.writeBlocking([tagPath], [value])
        
    except Exception as e:
        logger = system.util.getLogger("ButtonScript")
        logger.error("Error: " + str(e))
```

### Startup Script (View)
```python
def onStartup(self):
    # Initialize view custom properties
    self.view.custom.isLoading = True
    
    # Load initial data
    try:
        data = system.db.runNamedQuery("GetInitialData", {})
        self.view.custom.data = data
    finally:
        self.view.custom.isLoading = False
```

### Message Handler
```python
def onMessageReceived(self, payload):
    messageType = payload.get("type")
    
    if messageType == "refresh":
        self.view.custom.refreshTrigger += 1
    elif messageType == "select":
        itemId = payload.get("itemId")
        self.view.custom.selectedId = itemId
```

### Transform Script
```python
# value is the input from the binding
# self gives access to component (Perspective)

if value is None:
    return []

# Transform dataset to list of dicts
result = []
for row in system.dataset.toPyDataSet(value):
    result.append({
        "label": row["name"],
        "value": row["id"],
        "data": row
    })
return result
```

## Script Libraries

### Project Library Structure
```
project/
└── ignition/
    └── script-python/
        └── myproject/
            ├── __init__.py (resource.json)
            └── utils/
                ├── __init__.py (resource.json)
                └── code.py
```

### code.py Example
```python
# myproject/utils/code.py

def formatValue(value, decimals=2):
    """Format a numeric value with specified decimals."""
    if value is None:
        return "N/A"
    return "{:.{}f}".format(float(value), decimals)

def readTagSafe(tagPath, default=None):
    """Read tag with error handling."""
    try:
        result = system.tag.readBlocking([tagPath])[0]
        if result.quality.isGood():
            return result.value
        return default
    except:
        return default

def writeTagWithConfirm(tagPath, value, timeout=5000):
    """Write tag and verify the write succeeded."""
    import time
    system.tag.writeBlocking([tagPath], [value])
    start = time.time()
    while (time.time() - start) * 1000 < timeout:
        current = system.tag.readBlocking([tagPath])[0].value
        if current == value:
            return True
        system.util.sleep(100)
    return False
```

### Using Library Functions
```python
# In any script
from myproject.utils import formatValue, readTagSafe

value = readTagSafe("[default]MyTag", default=0)
display = formatValue(value, decimals=1)
```

### resource.json for Script Module
```json
{
  "scope": "A",
  "version": 1,
  "restricted": false,
  "overridable": true,
  "files": ["code.py"],
  "attributes": {
    "lastModification": {
      "actor": "admin",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  }
}
```
