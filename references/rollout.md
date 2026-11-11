# Small, reversible rollout

1. Record the main model, existing auxiliary route, account/plan, and current guard
   behavior. Save a backup without exposing secrets.
2. Discover available candidates and the task's capability/context requirements.
   Mark whether the cost order is verified or only a tentative tier inference.
3. Select the lowest capable candidate within the existing authorized destination.
   A small model needing repeated retries can cost more per completed task.
4. Use a native auxiliary route. If none exists, do not change the main model to
   simulate separate background routing. Explain the limitation.
5. Verify runtime resolution. Missing selected model => skip that auxiliary run,
   report once, and retain the foreground route; never silently use premium fallback.
6. Offline-test low-tier selection, unavailable model, insufficient context, missing
   tools, unverified ranking, unsupported host, and no-lower-tier scenarios.
7. Run at most a small bounded canary when needed. Do not allow canary memory writes,
   recursive reviews, endless fallback attempts, or uncapped tool execution. Use a
   bounded mock/read-only tool when verifying tool support; disabling every tool
   verifies only text routing, not tool-calling capability.
8. Reload every relevant gateway, worker, and desktop/web backend. Verify each
   actual profile and execution path, not only an administrator's test process.
9. Roll back the narrow auxiliary setting if quality fails. Keep the stopped-job
   latch and cost controls; do not raise safety limits as a routing workaround.

## Result labels

- **Configured:** a supported auxiliary setting was written.
- **Runtime verified:** actual dispatch used the chosen provider/model and met the
  required capability/quality check.
- **Recommendation only:** configuration access or native routing is unavailable.
- **Savings unmeasured:** no reliable account-level cost delta has been measured.
