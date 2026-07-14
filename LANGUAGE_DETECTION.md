# Language detection

Language detection consumes the inspected filesystem inventory and configuration to identify supported languages without assuming one language or one layout. A candidate can contain multiple languages simultaneously.

Generation 1 adapter planning targets Python, C#, Swift, JavaScript, TypeScript, C, and C++. Detection records the language identity, supporting observations, confidence, and applicable adapters; it does not itself measure quality.

Explicit configuration may constrain or supplement detection but cannot silently assert support for an unavailable adapter. Unknown, conflicting, or unsupported language states remain explicit inputs to capability and adapter planning.
