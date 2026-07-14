# Complexity adapters

Implemented: `complexity.radon` 0.1.0 using externally provisioned, explicitly pinned `radon==6.0.1` for Python. The adapter discovers `radon` from the isolated execution environment, records its resolved version, rejects unavailable or pre-6.0 versions, and normalizes native paths before evidence persistence. Planned selections: Lizard for C/C++, Roslyn for C#, ESLint for JavaScript/TypeScript, and Swift tooling for Swift. The Runtime discovers only capability/adapter identity and never analyzer names.
