# LEGO Spike Prime Simulator - Code Documentation

## Overview

This is a web-based simulator for testing Python code before deploying it to real LEGO Spike Prime robots. The application runs entirely in the browser using Vue 3 for the UI framework and Pyodide for executing Python code via WebAssembly.

## Source Files

| File | Purpose |
|------|---------|
| `src/main.js` | Vue application entry point |
| `src/App.vue` | Root component, orchestrates the application |
| `src/components/CodeInput.vue` | Python code editor with Run button |
| `src/components/Console.vue` | Output log display |
| `src/composables/useRobotState.js` | Robot state management (motors, logs) |
| `src/composables/usePyodide.js` | Python execution engine via Pyodide |

---

# Input and Output

## Input

### Command-line Flags
This is a client-side web application with no command-line interface. Development commands are:
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Configuration
| Source | Configuration |
|--------|---------------|
| `vite.config.js` | Vite build configuration with Vue plugin |
| `package.json` | Dependencies (Vue 3, Pyodide, Vite) |
| `usePyodide.js:45` | Pyodide CDN URL: `https://cdn.jsdelivr.net/pyodide/v0.27.0/full/` |

### Data Received from External Services
| Service | Data | Purpose |
|---------|------|---------|
| Pyodide CDN (jsdelivr.net) | WebAssembly Python runtime | Enables Python execution in browser |

### User Input
| Component | Input Type | Description |
|-----------|------------|-------------|
| `CodeInput.vue` | Text (textarea) | Python code entered by user |
| `CodeInput.vue` | Click (button) | "Run Code" button triggers execution |
| `Console.vue` | Click (button) | "Clear" button clears log output |

## Output

### Data Displayed on Screen
| Component | Output | Description |
|-----------|--------|-------------|
| `App.vue` header | Status badge | "Loading Pyodide...", "Ready", or "Error" |
| `Console.vue` | Log entries | Timestamped messages from code execution |

### Log Entry Format
```
[HH:MM:SS] <message>
```

### Types of Log Messages
- `Pyodide initialized successfully` - Initialization complete
- `--- Running code ---` - Code execution started
- `Motor <port> running at <velocity> deg/sec` - Motor started
- `Motor <port> stopped` - Motor stopped
- `--- Code execution complete ---` - Code finished
- `Error: <message>` - Execution error

### Data Sent to External Services
None. This application is fully client-side and does not send data to any external services.

---

# Architecture

## PlantUML Class Diagram

```plantuml
@startuml
skinparam classAttributeIconSize 0

package "Vue Components" {
  class App {
    -state: RobotState
    -isLoading: Ref<boolean>
    -isReady: Ref<boolean>
    +handleRunCode(code: string): void
    +handleClearConsole(): void
  }

  class CodeInput {
    -code: Ref<string>
    -disabled: boolean
    +emit('run', code): void
  }

  class Console {
    -logs: Array<LogEntry>
    -consoleRef: Ref<HTMLElement>
    +emit('clear'): void
  }
}

package "Composables" {
  class useRobotState {
    -state: reactive
    +PORTS: Object
    +motorRun(port, velocity): void
    +motorStop(port): void
    +motorVelocity(port): number
    +addLog(message): void
    +clearLogs(): void
    +resetState(): void
  }

  class usePyodide {
    -pyodide: ShallowRef
    -isLoading: Ref<boolean>
    -isReady: Ref<boolean>
    -error: Ref<string>
    +initPyodide(): Promise<void>
    +runCode(code): Promise<void>
  }
}

package "State" {
  class RobotState {
    +motors: Object
    +logs: Array<LogEntry>
  }

  class MotorState {
    +velocity: number
    +absolutePosition: number
    +relativePosition: number
    +running: boolean
  }

  class LogEntry {
    +timestamp: string
    +message: string
  }
}

package "External" {
  class Pyodide {
    +runPythonAsync(code): Promise
    +globals: Map
  }
}

App --> CodeInput : contains
App --> Console : contains
App --> useRobotState : uses
App --> usePyodide : uses

useRobotState --> RobotState : manages
RobotState --> MotorState : contains 6
RobotState --> LogEntry : contains many

usePyodide --> Pyodide : wraps
usePyodide --> useRobotState : calls motor functions

CodeInput ..> App : emits 'run'
Console ..> App : emits 'clear'

@enduml
```

## Component Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                        App.vue                              │
│  ┌─────────────────────┐    ┌─────────────────────────┐    │
│  │   useRobotState()   │    │     usePyodide()        │    │
│  │   - state           │◄───│     - initPyodide()     │    │
│  │   - clearLogs()     │    │     - runCode()         │    │
│  │   - motorRun()      │    │     - isReady           │    │
│  └─────────────────────┘    └─────────────────────────┘    │
│             │                           │                   │
│             ▼                           ▼                   │
│  ┌─────────────────────┐    ┌─────────────────────────┐    │
│  │    Console.vue      │    │    CodeInput.vue        │    │
│  │    :logs="state.    │    │    :disabled="!isReady" │    │
│  │         logs"       │    │    @run="handleRunCode" │    │
│  │    @clear="handle   │    └─────────────────────────┘    │
│  │      ClearConsole"  │                                    │
│  └─────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘
```

---

# Lifecycle of Objects

## Application Lifecycle

### Phase 1: Initialization
1. Browser loads `index.html`
2. Vite serves `src/main.js`
3. Vue creates app instance and mounts `App.vue`
4. `onMounted()` hook triggers `initPyodide()`
5. Pyodide runtime loads from CDN
6. Python modules (`hub.port`, `motor`) are created
7. Status changes from "Loading..." to "Ready"

### Phase 2: User Interaction
1. User enters Python code in textarea
2. User clicks "Run Code"
3. Code executes via Pyodide
4. Motor functions update robot state
5. Logs appear in Console

### Phase 3: Cleanup
1. User clicks "Clear" to reset logs
2. User can run new code

## PlantUML Sequence Diagram - Initialization

```plantuml
@startuml
title Application Initialization Sequence

participant Browser
participant "main.js" as Main
participant "App.vue" as App
participant "usePyodide" as Pyodide
participant "useRobotState" as State
participant "CDN" as CDN

Browser -> Main: Load application
Main -> App: createApp().mount()
activate App

App -> State: useRobotState()
State --> App: { state, clearLogs, ... }

App -> Pyodide: usePyodide()
Pyodide --> App: { isLoading, initPyodide, ... }

App -> App: onMounted()
App -> Pyodide: initPyodide()
activate Pyodide

Pyodide -> Pyodide: isLoading = true
Pyodide -> CDN: loadPyodide(indexURL)
CDN --> Pyodide: Pyodide runtime (WASM)

Pyodide -> Pyodide: Expose JS functions to Python\n(motorRun, motorStop, etc.)
Pyodide -> Pyodide: Create hub.port module
Pyodide -> Pyodide: Create motor module
Pyodide -> Pyodide: Override sys.stdout/stderr

Pyodide -> State: addLog("Pyodide initialized")
Pyodide -> Pyodide: isReady = true
Pyodide -> Pyodide: isLoading = false
deactivate Pyodide

App -> App: UI updates to "Ready"
deactivate App

@enduml
```

## PlantUML Sequence Diagram - Code Execution

```plantuml
@startuml
title Code Execution Lifecycle

actor User
participant "CodeInput.vue" as CodeInput
participant "App.vue" as App
participant "usePyodide" as Pyodide
participant "Pyodide Runtime" as Runtime
participant "Python motor module" as Motor
participant "useRobotState" as State
participant "Console.vue" as Console

User -> CodeInput: Enter Python code
User -> CodeInput: Click "Run Code"
CodeInput -> App: emit('run', code)

App -> Pyodide: runCode(code)
activate Pyodide

Pyodide -> State: addLog("--- Running code ---")
State -> Console: logs updated (reactive)
Console -> Console: Auto-scroll

Pyodide -> Runtime: runPythonAsync(code)
activate Runtime

Runtime -> Motor: motor.run(port.A, 1000)
Motor -> State: _motor_run(0, 1000)
State -> State: motors[0].velocity = 1000
State -> State: motors[0].running = true
State -> State: addLog("Motor A running...")
State -> Console: logs updated (reactive)
Console -> Console: Auto-scroll

Runtime --> Pyodide: execution complete
deactivate Runtime

Pyodide -> State: addLog("--- Code execution complete ---")
State -> Console: logs updated (reactive)
deactivate Pyodide

@enduml
```

---

# Event Handling Logic

## Events Overview

| Event | Source | Handler | Action |
|-------|--------|---------|--------|
| Component mounted | Vue lifecycle | `App.onMounted()` | Initialize Pyodide |
| Run button click | `CodeInput.vue` | `App.handleRunCode()` | Execute Python code |
| Clear button click | `Console.vue` | `App.handleClearConsole()` | Clear log entries |
| Logs array change | `useRobotState` | `Console.watch()` | Auto-scroll to bottom |
| Code textarea input | User | `v-model` binding | Update `code` ref |

## Event Flow Diagrams

### Run Code Event

```plantuml
@startuml
title Run Code Event Flow

start
:User clicks "Run Code" button;
:CodeInput.handleRun() called;
:emit('run', code.value);
:App receives @run event;
:App.handleRunCode(code) called;
:usePyodide.runCode(code) called;

if (pyodide ready?) then (yes)
  :addLog("--- Running code ---");
  :pyodide.runPythonAsync(code);

  if (execution successful?) then (yes)
    :addLog("--- Code execution complete ---");
  else (no)
    :addLog("Error: " + message);
  endif
else (no)
  :addLog("Pyodide is not ready yet");
endif

stop
@enduml
```

### Clear Console Event

```plantuml
@startuml
title Clear Console Event Flow

start
:User clicks "Clear" button;
:Console.handleClear() called;
:emit('clear');
:App receives @clear event;
:App.handleClearConsole() called;
:useRobotState.clearLogs() called;
:state.logs.splice(0, length);
:Console reactively updates;
:Placeholder message shown;
stop
@enduml
```

### Auto-Scroll Event

```plantuml
@startuml
title Console Auto-Scroll Event Flow

start
:Log entry added to state.logs;
:Vue reactivity triggers watch();
:watch() detects logs.length change;
:await nextTick();
note right: Wait for DOM update
:Get consoleRef.value;
:Set scrollTop = scrollHeight;
:Console scrolls to bottom;
stop
@enduml
```

## Python-to-JavaScript Bridge Events

When Python code calls motor functions, the following bridge occurs:

```plantuml
@startuml
title Python-JavaScript Bridge

participant "Python Code" as Python
participant "motor module\n(Python)" as MotorPy
participant "Pyodide Bridge" as Bridge
participant "_motor_run\n(JavaScript)" as MotorJS
participant "useRobotState" as State

Python -> MotorPy: motor.run(port.A, 1000)
MotorPy -> Bridge: _motor_run(0, 1000)
note over Bridge: JavaScript function\nexposed via globals.set()
Bridge -> MotorJS: motorRun(0, 1000)
MotorJS -> State: state.motors[0].velocity = 1000
MotorJS -> State: state.motors[0].running = true
MotorJS -> State: addLog("Motor A running at 1000 deg/sec")

@enduml
```

## Vue Reactivity Flow

```
User Action
    │
    ▼
Event Handler (e.g., handleRunCode)
    │
    ▼
State Mutation (e.g., state.logs.push())
    │
    ▼
Vue Reactivity System detects change
    │
    ▼
Component re-renders (Console.vue)
    │
    ▼
DOM updated
    │
    ▼
watch() callbacks triggered (auto-scroll)
```
