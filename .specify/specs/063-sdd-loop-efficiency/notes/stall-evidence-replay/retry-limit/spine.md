# fixture line state spine
dispatch stage=attempt-0
retry_consumed=1 reason=FAILED
dispatch stage=attempt-1
retry_consumed=2 reason=FAILED
dispatch stage=attempt-2
stall_state=stalled-retry-limit
retries_consumed=2
