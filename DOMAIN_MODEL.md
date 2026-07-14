# Domain model

The canonical domain model defines stable, language-neutral identities for product/runtime, repository, workspace, candidate, file, module, type, function, language, capability, adapter, analyzer, measurement, finding, policy, baseline, comparison, evidence, and report.

Repository identity supports a local path representation, canonical name where known, optional remote URL, optional source-control metadata, and use without Git. Candidate identity declares `git_commit`, `content_digest`, or `declared`, with a validation status; a Git SHA is never assumed. Portable evidence uses normalized relative paths and policy-controlled redaction, never absolute local paths by default.

Files and symbols use stable local identifiers, normalized paths, language, kind, display and qualified names, optional parent, location, and analyzer identity. Language- or analyzer-specific data belongs only in owned namespaced extensions.
