## Copilot-for-Xcode — quick onboarding for AI coding agents

This file gives concise, repo-specific guidance so an AI agent can be productive immediately.

Goals
- Understand the multi-process Xcode architecture (host app, XPC services, editor extension).
- Know the canonical local build/run steps and important files to edit.
- Recognize cross-component contracts (XPC service name, entitlements, versioning).

Key components (big picture)
- `Copilot for Xcode/` — the host macOS app (settings UI, ships the extension host). See `Version.xcconfig` for centralized versioning.
- `EditorExtension/` — Xcode Source Editor Extension. It only forwards editor content to an XPC service and applies returned edits. Primary file: `EditorExtension/SourceEditorExtension.swift`.
- `ExtensionService/` + `CommunicationBridge/` — non-sandboxed background services that implement most features and maintain XPC communication. Important files: `ExtensionService/ServiceDelegate.swift`, `ExtensionService/XPCController.swift`, `CommunicationBridge/main.swift`.
- `Core/` and `Tool/` — Swift packages containing the main logic used by the services and host app. `Core/Sources/` contains core behavior; `Tool/` has command-line helpers.
- `Server/` — local web UI and language server bundling. Uses `webpack` and `@github/copilot-language-server` packages.

Developer workflows (explicit commands)
- Local macOS app build (clean & build):
  - From repo root: `sh ./Script/uninstall-app.sh && rm -rf ./build && sh ./Script/localbuild-app.sh` — this produces `GitHub Copilot for Xcode.app` in `build/`.
  - Note: The build run scripts expect `node`/`npm` on PATH. The repo historically recommends symlinking system `node`/`npm` into `/usr/local/bin` (see `DEVELOPMENT.md`).
- Run server build (for Server UI / language server packaging):
  - `cd Server && npm ci && npm run build` (script maps to `webpack`).
- Testing the Source Editor Extension:
  - Launch `ExtensionService`, `CommunicationBridge` and the `EditorExtension` target in Xcode (see Apple docs: "Testing Your Source Editor Extension").
- Unit tests / test plan:
  - Run tests from the `Copilot for Xcode` target in Xcode. New tests should be added to `TestPlan.xctestplan`.

Project-specific conventions & gotchas
- XPC contract: the editor extension is sandboxed and must call a trusted non-sandboxed XPC service. The XPC service name must be listed in `com.apple.security.temporary-exception.mach-lookup.global-name` entitlements. When renaming services, update entitlements and both sides (see `ExtensionService` and `CommunicationBridge`).
- Versioning: all target versions are controlled in `Version.xcconfig`. Change it there rather than editing target plist files directly.
- Build scripts use a limited PATH: ensure `node` and `npm` are resolvable by run scripts (see `DEVELOPMENT.md` symlink suggestion) to avoid Xcode build-time failures.
- Swift formatting: the project uses `swiftformat`. Follow the existing style (Ray Wenderlich guide with 4-space indentation) and the repo toolchain.
- Packaging for the server: `Server/package.json` contains architecture-specific language-server packages (`darwin-arm64` and `darwin-x64`). When updating the copilot language server, keep those in sync.

Integration points worth knowing
- XPC wiring: `CommunicationBridge/main.swift` ↔ `ExtensionService/*` ↔ `EditorExtension/` — these three are the most important files to trace when fixing editor-to-service bugs.
- Host ↔ Core: `Copilot for Xcode/` uses `Core` package APIs. Look in `Core/Sources/` for service and host API definitions (Service vs Host separation — `Service` implementations live under `Core`/`Service` and host implementations under `Core`/`HostApp`).
- Native UI vs server UI: Some tooling and debug UIs are bundled under `Server/` and built via `webpack`. The `Server` bundle is not required to build the macOS app but is used for dev/debugging the language server and web-based UIs.

Examples of common edits/tasks (where to look)
- Change XPC service name: update `ExtensionService` and `CommunicationBridge` code and the entitlements file (search for `mach-lookup` in the repo).
- Update app version: edit `Version.xcconfig`.
- Add server dependency or rebuild UI: `cd Server && npm ci && npm run build`.
- Local manual install: after `localbuild-app.sh`, copy `build/GitHub Copilot for Xcode.app` into `/Applications` to run and test.

Files to inspect first (fast path)
- `DEVELOPMENT.md` — local build notes and PATH caveat.
- `README.md` — user-facing overview and Agent Mode description.
- `ExtensionService/ServiceDelegate.swift`, `CommunicationBridge/main.swift`, `EditorExtension/SourceEditorExtension.swift` — XPC path.
- `Version.xcconfig`, `Script/localbuild-app.sh`, `Script/uninstall-app.sh`, `TestPlan.xctestplan`.
- `Server/package.json` and `Server/src/` for language server/web UI details.

If anything here is out-of-date or you rely on a different workflow (CI-only changes, alternate dev environment), tell me which steps to adjust and I will update this file.

— End of instructions
