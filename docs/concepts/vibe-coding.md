# Vibe Coding Development Guide

> **Document Type**: Development Guide  
> **Scope**: Spec Kit Project & AI-Native Development Paradigm  
> **Core Topics**: Architecture design and practice of Agents, Skills, and Tools

---

## 1. Core Concepts

### 1.1 Three Core Building Blocks

The AI-native development paradigm is built upon three layered, decoupled core building blocks:

```
┌─────────────────┐
│    Agent        │  ← Top Layer: Task Planning & Decision-Making
│    (Agent)      │
├─────────────────┤
│    Skill        │  ← Middle Layer: Domain Knowledge & Behavior Guidelines
│    (Skill)      │
├─────────────────┤
│    Tool         │  ← Bottom Layer: Atomic Operation Execution
│    (Tool)       │
└─────────────────┘
```

---

### 1.2 Agent

**Definition**: An autonomous/semi-autonomous system with an LLM as its core brain, responsible for task planning and orchestration.

**Core Responsibilities**:
- Receive high-level goals from developers
- Perform intent parsing and task decomposition
- Formulate step-by-step execution plans
- Select and invoke skills and tools
- Monitor execution progress and dynamically adjust strategies

**Key Capabilities**:
- ✅ Contextual reasoning
- ✅ Task planning and orchestration
- ✅ Decision-making and tool selection
- ✅ Multi-step task coordination

**Example Scenario**: 
GitHub Copilot Agent Mode understands user intent and decides which skills and tools to invoke to complete end-to-end feature implementation.

---

### 1.3 Skill

**Definition**: A reusable capability package oriented toward specific tasks, containing instructions and resources, typically existing as a directory with a `SKILL.md` file.

**Directory Structure**:
```
skills/
└── my-skill/
    ├── SKILL.md          # Required: Skill description file
    ├── scripts/          # Optional: Helper scripts
    └── reference/        # Optional: Reference materials
```

**Core Responsibilities**:
- Provide specialized domain knowledge
- Define behavioral norms and operational guidelines
- Constrain agent behavior in specific scenarios

**Key Characteristics**:
- ✅ **Reusable**: Define once, use many times
- ✅ **Declarative**: Declare rules via `SKILL.md`
- ✅ **Encapsulated**: Encapsulate domain-specific knowledge
- ✅ **Controllable**: Enhance predictability of AI behavior

**Purpose**: 
Externalize implicit development experience into shared team knowledge assets, ensuring AI-generated code quality and consistency.

---

### 1.4 Tool

**Definition**: A collection of low-level functions that can be invoked to perform specific actions, serving as the interface between agents and the external environment.

**Manifestations**:
- Shell functions and system commands
- Services provided by MCP (Model Context Protocol) servers
- Code interpreters
- API call interfaces

**Core Responsibilities**:
- Execute atomic engineering operations
- File read/write, API calls
- System command execution
- Git operations, test execution, etc.

**Key Characteristics**:
- ✅ **Atomic**: Single responsibility, clear functionality
- ✅ **Functional**: Directly produces observable results
- ✅ **Programmable**: Callable by agents
- ✅ **Execution Unit**: The final landing point of agent plans

---

### 1.5 Quick Comparison of Building Blocks

| Building Block | Role | Responsibility | Characteristics |
| :--- | :--- | :--- | :--- |
| **Agent** | Commander | Task planning, decision-making, orchestration | Reasoning, planning, decision-making |
| **Skill** | Strategy Library | Provide norms, guidelines, constraints | Reusable, declarative |
| **Tool** | Executor | Execute concrete operations | Atomic, functional |

---

## 2. Interaction Mechanisms & Responsibility Boundaries

### 2.1 Interaction Flow

```
Developer Intent → Agent Parsing → Task Planning → Skill Loading → Tool Invocation → Execution Feedback → Result Validation
```

**Detailed Flow**:

1. **Intent Input**: Developer presents a high-level goal to the agent (which may be vague)
2. **Intent Parsing**: Agent combines context to parse, clarify, and refine the goal
3. **Task Planning**: Formulate a detailed step-by-step execution plan
4. **Skill Matching**: Identify subtasks requiring domain-specific knowledge, load corresponding skills
5. **Tool Invocation**: Translate the plan into concrete tool calls
6. **Execution Feedback**: Tools return results after execution (success/failure/output)
7. **Iterative Optimization**: Agent evaluates results and adjusts subsequent plans accordingly

---

### 2.2 Responsibility Boundaries

#### Agent vs Skill

| Dimension | Agent | Skill |
| :--- | :--- | :--- |
| **Responsibility** | Macro-level "what to do" and "how to do it" | Micro-level "how it should be done" and "what must not be done" |
| **Nature** | Dynamic, adaptive decision engine | Relatively static, reusable knowledge configuration file |
| **Focus** | Overall task planning and scheduling | Behavioral norms and constraints for specific tasks |

#### Skill vs Tool

| Dimension | Skill | Tool |
| :--- | :--- | :--- |
| **Responsibility** | High-level, rule-based instruction set | Single, atomic functional unit |
| **Complexity** | May involve multiple steps | Single operation |
| **Relationship** | May invoke multiple tools to collaboratively complete tasks | Invoked by skills or agents |

**Example**: 
The "Deploy Microservice" skill may invoke in sequence:
1. Build Docker image (Tool 1)
2. Push image to registry (Tool 2)
3. Deploy on Kubernetes (Tool 3)

#### Agent vs Tool

| Dimension | Agent | Tool |
| :--- | :--- | :--- |
| **Responsibility** | Decision authority: when, why, which tool to invoke | Execution: faithfully execute instructions, no autonomous decisions |
| **Management** | Discover and manage tools via protocols like MCP | Not all tools directly exposed to LLM |
| **Goal** | Ensure security and controllability | Focus on execution efficiency |

---

## 3. The Core Role of the MCP Protocol

### 3.1 What is MCP

**MCP (Model Context Protocol)** is an open standard protocol designed specifically to solve the tool access problem, positioned as the "connector" and "standardizer" of the AI ecosystem.

**Core Goal**: 
Like USB-C for electronic devices, provide a unified interface so agents can "plug and play" access to different tools and services.

---

### 3.2 MCP Architecture Model

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│     Host     │ ←→ │    Client    │ ←→ │    Server    │
│ (IDE/Editor) │    │ (IDE Component)│   │ (Tool Service)│
└──────────────┘    └──────────────┘    └──────────────┘
```

**Technical Specifications**:
- **Message Format**: JSON-RPC 2.0
- **Message Types**: Request, Response, Notification
- **Lifecycle**: Initialization → Operation → Shutdown

---

### 3.3 Core Value of MCP

#### ✅ High Decoupling & Interoperability
- Skills and tools are decoupled from specific development environments (VS Code, Cursor, etc.)
- MCP-compliant skills can run in any MCP-supporting IDE
- Enhances skill portability and ecosystem extensibility

#### ✅ Security & Permission Management
- **Capability Negotiation**: Declare and negotiate supported feature sets upon connection
  - Accessible filesystem paths (roots)
  - Available tool list (tools)
  - Readable resources (resources)
- **Principle of Least Privilege**: Prevent data corruption risks from privilege abuse

#### ✅ Standardized Tool Discovery & Invocation
- Built-in `tools/list` and `tools/call` standard methods
- Agents dynamically discover and invoke remote/local tools
- No need to hardcode tool details
- Supports complex distributed multi-agent systems

#### ✅ Ecosystem Catalyst
- GitHub Copilot's success benefits from MCP support
- A marketplace around MCP Servers is forming
- Developers can easily discover, install, and share specialized skills

---

## 4. From Vibe Coding to Agentic Engineering

### 4.1 Evolution Path Comparison

| Dimension | Vibe Coding | Agentic Engineering |
| :--- | :--- | :--- |
| **Developer Role** | Prompter, director, co-pilot | Architect, project manager, supervisor |
| **Interaction Mode** | Tightly iterative "goal satisfaction loop" | Goal delegation and monitoring |
| **Task Scope** | Component-level (functions, UI elements, scripts) | Feature-level/app-level (end-to-end functionality, system migration) |
| **Tool Usage** | Code generation, other tools triggered manually | Agents autonomously and systematically interact |
| **Automation Level** | Semi-automated, high human-machine collaboration | Highly automated |

---

### 4.2 Characteristics of Vibe Coding

**Advantages**:
- ✅ Lowers the barrier to AI programming
- ✅ Cultivates developer intuition for AI collaboration
- ✅ Accelerates development progress
- ✅ Suitable for rapid prototyping and creative exploration

**Limitations**:
- ❌ High developer involvement, time-consuming
- ❌ Limited task scope
- ❌ Tool usage requires manual management

---

### 4.3 Characteristics of Agentic Engineering

**Core Transformation**:
- Developers no longer concern themselves with specific implementation details
- Delegate complex high-level goals to AI agents
- Supervise and validate agent execution process and outputs

**Capability Scope**:
- ✅ End-to-end feature implementation
- ✅ Complex cross-file refactoring
- ✅ System migration
- ✅ Comprehensive CI/CD pipeline automation

---

### 4.4 The Methodological Bridge

The methodology presented in this document (clearly defining agents, skills, tools, and their interactions) is the **necessary path** from Vibe Coding to Agentic Engineering:

```
Vibe Coding → [Structured Methodology] → Agentic Engineering
              ↓
        Preserve autonomy
        Provide controllability
        Ensure security
```

**Core Value**:
- Provide a solid foundation for agent autonomy
- Ensure agents behave within preset rules and constraints
- Achieve balance between autonomy and controllability

---

## 5. Core Design Principles

### 5.1 Layered Decoupling Principle

**Requirement**: Strictly separate the three layers of Agent (command), Skill (strategy), and Tool (execution)

**Goal**: 
- Keep each layer's responsibilities singular and independent
- Avoid functional redundancy and coupling
- Improve system maintainability

---

### 5.2 Standardization-First Principle

**Requirement**: Prioritize MCP as the default communication standard for agent interaction with the external environment

**Goal**:
- Ensure the openness of skills and tools
- Ensure interoperability
- Avoid vendor lock-in to specific platforms

---

### 5.3 Declarative Over Imperative Principle

**Requirement**: Use skills (specifically `SKILL.md` files) as a declarative way to define behavioral norms

**Advantages**:
- ✅ Significantly improved reusability
- ✅ Improved reliability
- ✅ Improved maintainability
- ✅ Avoid exhausting all details in prompts

---

### 5.4 Security-First Principle

**Requirement**: 
- Fully leverage MCP's capability negotiation mechanism
- Utilize GitHub Copilot CLI's tool permission controls
- Always adhere to the principle of least privilege

**Goal**: Guard against potential security risks

---

### 5.5 Iteration & Feedback Principle

**Requirement**: 
- Accept the non-deterministic nature of AI generation processes
- Establish rapid validation (e.g., automated testing) and feedback loops
- Continuously collect execution result data

**Goal**: Optimize agent planning capabilities and skill instruction effectiveness

---

## 6. Practice Guide

### 6.1 Define Agent Roles

**Action**: Create different types of agents based on project needs

**Examples**:
- 🎯 **Architect Agent**: Focuses on high-level planning
- 💻 **Developer Agent**: Focuses on code generation
- 🧪 **Test Agent**: Focuses on writing and executing test cases

**Value**: Achieve specialized division of labor in the development workflow, improving task execution efficiency and quality

---

### 6.2 Build Domain-Specific Skill Libraries

**Action**: Create skills around team tech stacks, coding standards, internal APIs, and business logic

**Location**: `.github/skills/` directory

**Requirement**: Each skill should have a detailed `SKILL.md` containing:
- Purpose description
- Input parameters
- Expected output
- Usage examples

**Value**: 
- Externalize implicit knowledge
- Ensure consistency and controllability of AI behavior
- Improve code quality

---

### 6.3 Actively Embrace the MCP Server Ecosystem

**Action**:
- Use existing MCP servers (e.g., GitHub MCP Server)
- Encourage teams to develop their own MCP servers

**What to Encapsulate**:
- Internal shell scripts
- Nushell modules
- Custom tools

**Value**: 
- Expand the capability boundaries of agents
- Break platform barriers
- Build an open, pluggable ecosystem

---

### 6.4 AI-Enable Traditional DevOps Processes

**Action**:
1. Decompose CI/CD processes (build, test, deploy) into atomic tools
2. Write corresponding skills for each toolchain segment
3. Create "Ops Agents" capable of autonomously completing full release workflows

**Value**:
- Achieve high automation in software delivery workflows
- Reduce manual intervention
- Accelerate release velocity

---

### 6.5 Systematically Record & Review Sessions

**Action**: Record the complete context of every AI interaction

**What to Record**:
- Generated plans
- Checkpoints
- Tool invocation history
- Execution results

**Value**:
- Valuable basis for debugging and tracing issues
- Accumulate experience
- Raw data source for training better agents

---

### 6.6 Practice Guide Quick Reference

| Guide | Specific Action | Goal & Value |
| :--- | :--- | :--- |
| **Define Agent Roles** | Create "Architect", "Developer", "Test Engineer" agents | Specialized division of labor, improved efficiency |
| **Build Skill Library** | Create skill packages in `.github/skills/` | Ensure consistency and controllability |
| **Expand MCP Ecosystem** | Use and develop MCP Servers | Expand capability boundaries |
| **AI-Enable DevOps** | Decompose CI/CD into atomic tools | High automation |
| **Record Sessions** | Record complete interaction context | Accumulate optimization data |

---

## 7. Summary

By systematically defining and analyzing the three core building blocks of **Agent**, **Skill**, and **Tool**, and following the core design principles and practice guides, developers can build a robust, efficient, and secure AI-native development paradigm.

**Core Contributions of the Methodology**:
1. ✅ Addresses many challenges facing AI programming today
2. ✅ Paints a clear blueprint for the future of software development
3. ✅ Drives the industry from artisanal workshop models toward industrialized, intelligent production

**Ultimate Goal**: 
Shift developers' attention from low-level syntax and algorithm implementation to higher-level goal definition, workflow orchestration, and quality assurance.

---

> **Related Documents**:
> - [Spec-Driven Development](./spec-driven.md)
> - [Constitution](../../memory/constitution.md)
> - [Feature Index](../../memory/features.md)
