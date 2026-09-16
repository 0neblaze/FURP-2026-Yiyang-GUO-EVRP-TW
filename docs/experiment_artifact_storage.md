# Experiment Artifact Storage Rules: v2 Policy, v3 Physical Schema, and Historical Compatibility

These rules govern experiment artifacts for Stages 0–8. They constrain only artifact
persistence; they do not change the algorithmic semantics of ALNS, `evrptw.objective`,
the unified validator, vehicle-first acceptance, or exact charging.

## Current availability

The repository retains `artifact-storage-v2` as the storage policy, defined in
`src/evrptw/artifacts.py`; the current physical evidence uses `screening_decisions_v3`
and continues to read v1, older v2, and legacy evidence. Every benchmark stage maintains a
single current code base; its internal gates are sequential steps, not separate versions. The historical
statuses, failure reasons, and prerequisite relations of specific attempts are
recorded in raw manifests, the retention registry, and the change log — not
hard-coded into long-term policy.

Every gate must bind a reviewed direct predecessor, a clean commit, and a frozen
wheel runtime; the actually selected workers/backend can only be decided by the
current raw review. `attemptNN`/`rerunNN` is the unique run identity, not a code
version.

The fixed policy fields for v1/v2:

| Field | Fixed value |
| --- | --- |
| `storage_policy_version` | `artifact-storage-v1` or `artifact-storage-v2` |
| `screening_schema_version` | `screening_decisions_v3` for new evidence; older v2 remains readable |
| `event_format` | `parquet` |
| `compression` | `zstd` |
| `compression_level` | `3` for v1; `1` for accepted v2 |
| `critical_evidence` | `full` |
| `diagnostic_evidence` | `aggregate` |
| `per_instance_seed_max_bytes` | `2 GiB` |
| `per_run_max_bytes` | `32 GiB` |

Every new runner must provide an enabled `[artifact_storage]` and write or read
artifacts through the shared writer/reader. Missing, disabled, legacy-format, or
unsupported parameters must fail before startup. Runners must not reimplement
event, checksum, or manifest logic.

## Shared physical layout

`run_label` must match `stageNN[_minor]_component_attemptNN` or `rerunNN`:

```text
results/<run_label>/
  control/
    <canonical>_run_metadata.json
    <canonical>_config.toml
    <canonical>_manifest.json
    <canonical>_manifest.sha256
  <instance>/<seed>/
    <canonical>_raw_<instance>_<seed>.json
    <canonical>_solution_<instance>_<seed>.json
    <canonical>_trace_<instance>_<seed>.json
    <canonical>_events_<instance>_<seed>.parquet
    <canonical>_route_dictionary_<instance>_<seed>.parquet
    <canonical>_screening_checks_<instance>_<seed>.parquet
    <canonical>_diagnostic_<instance>_<seed>.parquet
    <canonical>_environment_<instance>_<seed>.json
    <canonical>_failure_<instance>_<seed>.json
    <canonical>_shard_manifest_<instance>_<seed>.json
    <canonical>_shard_manifest_<instance>_<seed>.sha256
  review/
```

v1 does not require the shard manifest; the last two items were added by v2. Layered
campaigns add internal batch directories such as `batch0001` under the
top-level canonical run, and registers the logical path, root alias, volume
identity, byte count, and checksum through signed campaign/batch manifests; a batch
must not masquerade as a new attempt. `failure` files may be omitted when not
applicable, but the manifest must record `artifact_status.failure=not_applicable`.
All raw evidence is first written to a Git-ignored active staging root; after the
run is sealed, the retention interface verifies the complete tree SHA-256 and byte
counts and moves it into the archive root's `history/<run_label>/`. Tracked
summaries can be published only by an independent reviewer after the raw replay
passes.

## Critical evidence and indexes

The critical evidence that must be retained event-by-event includes exact-call
started/completed, feasible/infeasible, screening decisions, failures, cache
lookup/store/hit/eviction/oversize, incremental propagation/fallback, deadlines,
execution errors, accepted candidates, global-best candidates, vehicle-count
changes, and every exact route evaluation.

Ordinary successful candidates, ordinary rejected candidates, repeated route
timings, operator-call totals, and diagnostics by `run/lane/iteration/operator/
reason` may go into the `diagnostic.parquet` aggregates. Aggregation must not delete
or alter critical events, nor affect the validator, objective, exact-call
ordering, or failure replay. Route sequences are stored exactly once in
`route_dictionary.parquet`; events use integer route/lane/operator IDs.

Parquet uses an explicit Arrow schema and dictionary encoding; v1 uses Zstandard
level 3 and accepted v2 uses level 1. The lane/operator dictionaries go into the
trace index and the route dictionary into its own route-dictionary file; v2
streaming must not change these encoding and indexing semantics.

A cache lookup and its immediately following hit/miss result are stored as a single
`lookup_result` record in the physical event file. Old JSON/JSONL events keep their
original two-event semantics when read. `trace.json` is the trace index — it stores
only counters, configuration, dictionaries, Parquet references, and the schema
fingerprint; it does not re-embed the full event sets.

## The `artifact-storage-v2` implementation contract

### Streaming writer

- Parquet row groups are fixed at 65,536 rows; a single writer buffers at most 2
  row groups at a time;
- the event, route-dictionary, screening-definitions, screening-occurrences, and
  diagnostic streams each flush incrementally through typed column buffers — no
  dict-per-row hot paths and no accumulating the full run in a Python list first;
- `ArtifactStorageConfig(storage_policy_version="artifact-storage-v2")` is unlocked
  only after the v2 writer/reader, configuration validation, and tests all land;
- the writer lifecycle must cover `open shard → append → flush → finalize/abort`;
  exception paths must also close the writer and produce a partial manifest;
- the reader simultaneously supports v1 bundles, older v2 shards, the v3 physical
  schema, and immutable legacy bundles, restoring historical order through a
  streaming k-way merge.

### Shard ownership

- the unit of job parallelism is the independent `(instance, seed)` shard; a
  performance experiment containing the fixed four axes writes all four axes of
  the same pair into one shard; different time budgets in a benchmark become
  explicit axis/budget fields within the shard;
- a worker may write only its own shard — never run-level control files or another
  worker's directories;
- the parent may write run metadata, the control manifest, and the sidecar only
  after all worker states are settled, and must not read all event rows back into
  memory to merge;
- each shard independently records the schema fingerprint, row count, byte size,
  checksum, evidence completeness, worker identity, axis identity, and provenance;
- manifests are sorted by the canonical `(instance, seed)` key and do not depend on
  worker completion order.

### Deterministic identity

v2 event identity is determined by the canonical shard ordinal plus the
shard-local event ID. Reviewers replay using that composite identity and the
manifest order — never relying on process completion order, filesystem traversal
order, or exact Parquet byte equality. A rewritten Parquet needs only matching
schema and declared semantics, not byte equality.

### Interruption, budget overflow, and failure

On reaching the shard or run byte budget, the writer must flush/close the current
row group, seal the completed raw, solution, event, environment, and failure
evidence, mark the shard and run `evidence_completeness=partial`, write the
manifest/sidecar, and raise immediately. Silent truncation, overwriting, or a
serial fallback is forbidden. Partial, timeout, failure, and manifest-error runs are
all barred from publishing scientific summaries; their sealed directories move to
the external archive after the retention audit instead of accumulating unboundedly
in the workspace.

## The v2 replacement gate

A v2 storage replacement must simultaneously satisfy:

1. under the same fixed-work inputs, v1/v2 agree completely on validator, objective,
   critical-event, exact-call, candidate/cache, and failure semantics;
2. v1 history and existing bundles continue to pass the same reader/reviewer;
3. artifact persistence time does not exceed 36% of end-to-end time;
4. peak RSS does not exceed 50% of the v1 baseline;
5. partial/timeout/worker failures all produce verifiable shard manifests and fail
   fast;
6. an independent reviewer recomputes all summaries from raw shards and does not
   trust runner self-reported counts.

The current C run must complete the declared performance scope and fixed-work
equality, demonstrating that the expanded logical semantics are fully identical,
and meet the 36% persistence gate. Relations to any old physical schema,
remediation source, or failed predecessor are preserved only by manifests, the
retention registry, and the change log. Any later gate that breaks these
requirements must be marked `NOT_READY`; falling back to implicit v1 behavior or
lowering thresholds is forbidden.

## Historical compatibility

The Stage 0 frozen baseline, Stage 2/3 historical evidence, and published v1
bundles are not physically migrated, compressed, moved, or rewritten. They continue
to be read through the legacy/v1 reader and retain their true `storage_format`,
`retention_class`, `policy_compliance`, dirty, failure, and publication statuses in
the registry. Logical mapping does not imply copying or moving.

## Retention policy

- The retention policy fixes `workspace_full_evidence=active_only`; both
  complete and failed runs perform `archive`.
- The audit inventory records the run label, component, status, completeness,
  source commit, prerequisite identities, file count, total bytes, and tree
  SHA-256, signed with an independent sidecar.
- An archive must explicitly bind the inventory SHA-256 and be verified by the
  ignored storage-root locator for alias and volume identity. Same-volume moves use
  verified atomic renames; cross-volume moves first copy into a hidden temporary
  directory on the target volume, atomically place on the target volume after full
  re-verification, and only then clean the source. If the source directory changed
  after the audit, the target contents differ, or the post-migration re-verification
  fails, everything fails fast — and source data must never be deleted.
- active/unsealed runs cannot enter the inventory by default; only the
  pre-refactor historical migration may explicitly override, binding the expected
  directory count and total bytes at the same time. Registry updates must merge
  atomically by run label; overwriting historical rows is forbidden.
- The lightweight retention registry records only archive aliases
  and relative paths, never machine-local absolute paths. Detailed implementation
  changes are recorded through the retention registry and, for governance
  changes, in `AGENTS.md`.
- prerequisite/review calls `resolve_retained_run` with the run label; the registry
  and the local storage-root locator resolve the archive alias, re-verifying file
  counts, byte counts, and tree SHA-256 before returning to existing
  runners/reviewers. Callers must not concatenate paths themselves or store
  absolute archive paths in tracked files.
- Archived directories serve only as read-only comparison/prerequisite/replay
  inputs; a reviewer must not write a new review generation back into a registered
  archive tree, which would break the registry checksum. Raw evidence requiring a
  newly published generation must stay in the active root and be archived only
  after publication and sealing.

## Preflight before formal runs

Every new run must check the canonical label, attempt/rerun uniqueness, artifact
type, control configuration, manifest and sidecar,
source/config/instance/environment/reference provenance, Parquet schema
fingerprint, row count, byte size, shard identity, and raw-to-summary consistency.
An independent reviewer must first verify the run/shard manifests, then replay the
raw solutions, events, trace index, route dictionary, validator, and objective.

The `worker_identity` of a worker-owned shard must be the
PID of the actually executing process and must be findable in the same run's 50 ms
process-tree resource samples; multi-worker runs are forbidden from recording the
parent PID as the shard owner. The resource summary, raw/solution/trace, and
per-run CSVs must share exactly the same canonical scope; any missing, duplicated,
partial, or fallback marker fails fast.

The reviewer must also verify the canonical `(instance, seed) → shard_ordinal`
mapping, the bidirectional SHA-256 binding of every shard manifest with its own
sidecar, and the identical composite event identity in the trace index.
Performance axes must be serial and non-overlapping in configuration order;
finalisation may begin only after the last axis completes.

Re-reviews must not overwrite manifest-protected reports/findings in
place. New reports and findings are first written to
`review/generations/<content-sha256>/` and fsynced; only then is
`review_manifest.json` — the single trusted pointer — atomically replaced. The
manifest, report, and findings of the previously accepted review are archived under
`review/history/` keyed by the old manifest SHA-256. If publication is
interrupted, the old manifest and its referenced files remain verifiable, and
orphan generations do not count toward gates.

Reports must separate solver time, artifact persistence
time, and end-to-end time; CPU utilisation, chip power, kernel time, or compression
ratio alone cannot constitute a speedup conclusion.
