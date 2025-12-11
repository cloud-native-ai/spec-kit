# Quickstart: Remove GitHub API Integration

Since this is a removal feature, there is no "quickstart" for using it. However, developers can verify the removal as follows:

1. **Install the CLI**:
   ```bash
   pip install -e .
   ```

2. **Verify Command Removal**:
   ```bash
   speckit --help | grep taskstoissues
   # Should return no output
   ```

3. **Verify Error on Execution**:
   ```bash
   speckit taskstoissues
   # Should return "Error: No such command 'taskstoissues'."
   ```
