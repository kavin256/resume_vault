# Resume Vault - Development TODO

## Temporary Changes (To Revert Later)

### Chunked AI API Calls - TEMPORARY
- **Date**: 2024
- **File**: `backend/services/claude_provider.py`
- **Change**: Modified `tailor_resume` method to process work experiences one-by-one instead of sending all experiences in a single API call
- **Reason**: Reduce AI API payload size to prevent "request/response load too much" errors
- **Revert To**: 
  - Restore original `tailor_resume` method that sends all experiences in a single prompt
  - Remove the `_tailor_single_experience` and `_tailor_summary` helper methods
  - Remove chunked processing logic in `tailor_resume`

## Current Tasks

### High Priority
- [ ] Implement chunked API calls for resume tailoring (IN PROGRESS)

### Medium Priority
- [ ] Test chunked implementation for correctness
- [ ] Monitor AI API usage and costs

### Backlog
- [ ] Revert chunked changes once AI API limits are increased or alternative solution found
- [ ] Optimize prompt to reduce token usage while maintaining quality
