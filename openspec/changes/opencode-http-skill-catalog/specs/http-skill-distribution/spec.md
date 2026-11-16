# Spec Delta

## Purpose

Distribute released Devcraft skills through OpenCode's native HTTP catalog from the same canonical source used by the existing marketplaces.

## ADDED Requirements

### Requirement: Native catalog with complete standalone skills
The published catalog SHALL provide OpenCode's native index entries with skill name, version, and safe relative file paths. Each entry MUST include its entrypoint and all required supporting resources from the canonical released payload.

#### Scenario: OpenCode downloads a skill
- **WHEN** OpenCode resolves an entry from the catalog base URL
- **THEN** every listed file is available under that entry's skill directory and required resources resolve without an original checkout or another client's cache

### Requirement: Publish only the released payload
Catalog generation SHALL use the released canonical skill source and MUST NOT include proposals, private captures, evaluation outputs, bytecode caches, or unrelated repository content. Generated copies MUST remain build output, not separately maintained skill sources.

#### Scenario: Repository contains private or unreleased material
- **WHEN** a catalog is generated from a repository containing proposals, captures, and runtime caches
- **THEN** those files are absent from the published catalog and payload

### Requirement: Release version and source provenance agree
Each catalog entry SHALL use the shared released package version and include local provenance identifying its skill, release version, canonical source, and full source revision. Conflicting release inputs MUST fail generation rather than publish mislabeled content.

#### Scenario: Published source differs from the default branch
- **WHEN** a stable release is published while the default branch contains newer work
- **THEN** the catalog contains the tagged release's source, version, and revision

#### Scenario: Package versions disagree
- **WHEN** the release tag and applicable package manifests identify different versions
- **THEN** generation reports the mismatch and no new catalog is deployed

### Requirement: GitHub-hosted stable catalog
The distribution SHALL expose a stable HTTPS base URL through GitHub Pages and publish generated artifacts for stable GitHub releases. Drafts, prereleases, and ordinary development changes MUST NOT replace the stable catalog.

#### Scenario: Stable release publication
- **WHEN** an authorized stable GitHub release is published with matching source/version metadata
- **THEN** the publishing workflow builds the catalog from that release and deploys its generated artifact to the stable Pages location

### Requirement: Native installation lifecycle is documented
User documentation SHALL explain the catalog URL, native OpenCode configuration, version-driven updates, loaded provenance, explicit invocation, and removal of the source. It MUST distinguish this HTTP catalog from OpenChamber's Git-backed catalog and from native package plugins.

#### Scenario: User removes the catalog
- **WHEN** a user follows the documented uninstall procedure
- **THEN** the catalog source is removed from configuration without deleting canonical sources or unrelated skills, and remaining duplicate sources or already-loaded conversation content are explained

### Requirement: Publication checks are proportionate
Acceptance SHALL verify a valid index, reachable listed files, and native loading of a skill and supporting resource. It MUST NOT require investigation of OpenCode polling intervals, downloader internals, or transactional updates across independent skills.

#### Scenario: Catalog is ready to use
- **WHEN** the published files are reachable and an isolated OpenCode instance loads a skill and its resource
- **THEN** catalog delivery acceptance is satisfied without adding a multi-skill transaction guarantee
