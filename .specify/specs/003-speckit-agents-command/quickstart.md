# Quickstart: Speckit Agents Command

## Goal

Validate the planned behavior of `/speckit.agents` from requirements through contracts before task decomposition.

## Prerequisites

- Active branch: `003-speckit-agents-command`
- Existing requirements file:
  - `/storage/project/cloud-native-ai/spec-kit/.specify/specs/003-speckit-agents-command/requirements.md`
- Generated planning artifacts:
  - `plan.md`
  - `data-model.md`
  - `contracts/agents-command.openapi.yaml`

## Validation Steps

### Foundational Validation (Pre-US1)
1. **Confirm no unresolved clarifications**
   - Verify requirements contain no `[NEEDS CLARIFICATION]` markers.

2. **Validate overwrite behavior**
   - Ensure requirements and plan both state same-name agent updates overwrite existing files.

3. **Validate low-confidence inference behavior**
   - Ensure no-argument + low confidence flow stops generation and asks for one-sentence intent.

4. **Validate contradiction handling**
   - Ensure latest explicit user input is prioritized.
   - Ensure unresolved contradictions block save and request correction.

5. **Validate directory bootstrap behavior**
   - Ensure missing `.github/agents/` is auto-created before write.

6. **Validate least-privilege default tools**
   - Ensure unspecified `tools` yields minimal workflow-required set.

7. **Validate approved provider enforcement**
   - Ensure generated guidance allows only GitHub Copilot, Qwen Code, opencode.

### User Story 1 Validation (Create Custom AI Agent)
8. **Validate parameterized creation**
   - Test with explicit arguments: `/speckit.agents "Create a Python code reviewer agent"`
   - Verify agent file created with correct frontmatter and role definition

9. **Validate high-confidence inference creation**
   - Test without arguments in clear context: `/speckit.agents`
   - Verify agent created based on conversation context when confidence is high

10. **Validate low-confidence abort and intent request**
    - Test without arguments in ambiguous context: `/speckit.agents`
    - Verify system stops generation and requests one-sentence user intent

11. **Validate frontmatter structure**
    - Verify created agents have required fields: description, tools, model_hints, invocation
    - Verify YAML syntax is valid

12. **Validate example prompts**
    - Test the provided example prompts trigger appropriate agent creation

### User Story 2 Validation (Update Existing AI Agent)
13. **Validate same-name overwrite behavior**
    - Create an agent: `/speckit.agents "Create a test agent"`
    - Update the same agent: `/speckit.agents "Update the test agent with new capabilities"`
    - Verify original file is completely replaced, not merged

14. **Validate explicit input priority**
    - Create agent with inferred tools based on context
    - Update with explicit conflicting tool specification
    - Verify explicit tools take precedence over inferred ones

15. **Validate unresolved conflict handling**
    - Attempt update with contradictory explicit inputs
    - Verify system blocks save and requests user correction

### User Story 3 Validation (Validate Agent Quality and Consistency)
16. **Validate YAML syntax failure blocking**
    - Attempt to create agent with invalid YAML frontmatter
    - Verify save operation is blocked with specific error message

17. **Validate provider whitelist enforcement**
    - Attempt to create agent referencing unapproved provider (e.g., "Claude")
    - Verify save operation is blocked with approved providers list

18. **Validate tools-workflow consistency**
    - Create agent claiming capabilities without corresponding tools
    - Verify validation flags mismatch and blocks save

19. **Validate least-privilege tool inference**
    - Create agent without specifying tools
    - Verify minimal required tool set is automatically inferred and applied

20. **Validate error return structure**
    - Test various validation failures
    - Verify consistent error format with clear actionable messages

## Expected Outcome

- Requirements, plan, data model, and contract are consistent.
- Feature status and memory are updated to reflect planning completion.
- Repository is ready for `/speckit.tasks`.

## Manual Acceptance Test Results - US1

### Test 1: Parameterized Creation
- **Input**: `/speckit.agents "Create a Python code reviewer agent"`
- **Expected Result**: 
  - `.github/agents/python-code-reviewer.agent.md` created
  - Frontmatter contains required fields with appropriate values
  - Body defines clear role, constraints, workflow, and output format
  - Tools limited to least-privilege set for code review
- **Status**: ✅ Ready for implementation

### Test 2: High-Confidence Inference
- **Input**: `/speckit.agents` (in context of discussing code review needs)
- **Expected Result**: 
  - Agent created based on conversation context
  - Confidence level high enough to proceed without user intervention
- **Status**: ✅ Ready for implementation

### Test 3: Low-Confidence Abort
- **Input**: `/speckit.agents` (in ambiguous context)
- **Expected Result**: 
  - Generation stops immediately
  - Clear message requesting one-sentence user intent
  - No file created or modified
- **Status**: ✅ Ready for implementation

### Manual Acceptance Test Results - US3

### Test 4: YAML Validation Failure
- **Input**: Agent with malformed YAML frontmatter
- **Expected Result**: 
  - Clear error message indicating YAML syntax issue
  - No file created or modified
- **Status**: ✅ Ready for implementation

### Test 5: Provider Whitelist Enforcement  
- **Input**: Agent referencing "Claude" as provider
- **Expected Result**:
  - Clear error message listing approved providers only
  - No file created or modified
- **Status**: ✅ Ready for implementation

### Test 6: Tools-Workflow Consistency
- **Input**: Agent claiming file system access without file tools
- **Expected Result**:
  - Validation flags capability-tool mismatch
  - Clear guidance on required tools
- **Status**: ✅ Ready for implementation

### Test 7: Least-Privilege Tool Inference
- **Input**: Agent without explicit tools specification
- **Expected Result**:
  - Minimal tool set automatically inferred based on workflow
  - Tools limited to essential capabilities only
- **Status**: ✅ Ready for implementation

## Next Command

```text
/speckit.implement
```