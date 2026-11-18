# openai/plugins far from development: science and research
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in openai-platforms.md. Families here: `life-science-research`, `ngs-analysis`, `boltz-api-cli`, `zotero`.

## Family: life-science-research
- source path: `plugins/life-science-research` (v1.0.3, author OpenAI, license Proprietary)
- manifest notes: Codex-only (`.codex-plugin/plugin.json`); no Claude or Cursor manifest. No MCP server, app connector, hooks, commands or declared auth/install policy; the README says none are needed. Capabilities label: Interactive, Read, Write. Every lookup skill is a SKILL.md plus a bundled Python script that reads one JSON object on stdin (`echo '{...}' | python scripts/<script>.py`, path relative to the skill directory) and calls a public API: needs Python and outbound network; request inputs leave the machine. Default output is a compact markdown summary of a small first page (about 10 items); the full payload is saved only on request (`save_raw=true`, reported as `raw_output_path`). Lookups stop at source records: no statistics, modelling or analysis of measurements. No approval step. Exceptions are stated in the records.
- router: research-router-skill. Covers broad, mixed or unclear life-science questions across nine lanes (genetics/variants, locus-to-gene, expression, pathway/network/function, structure, chemistry/pharmacology, clinical/cancer, literature/datasets, omics). Sequence: understand objective -> normalize entities (gene/protein: ncbi-clinicaltables-skill, ensembl-skill, uniprot-skill; disease: efo-ontology-skill, opentargets-skill; variant: clinvar-variation-skill, ensembl-skill, PheWAS skills; compound: chembl-skill, pubchem-pug-skill, chebi-skill, hmdb-skill) -> pick 1-3 lanes and the minimum skills -> gather evidence (Codex subagents only if available and lanes are independent) -> synthesize. Gates: skip it for a narrow single-source lookup; no broad retrieval before entities are stable; do not overstate causality. A second entry, locus-to-gene-mapper-skill, is a fixed deterministic pipeline for ranked genes at GWAS loci.
- development distance: far (life-science research)
- disclosure: router-delegated. 50 skills total, including the router, mapper and BLAST workflow; records stay short for matching. None is relevant to ordinary software development.

### alphafold-skill
- id: life-science-research:alphafold-skill (source path: plugins/life-science-research/skills/alphafold-skill/SKILL.md)
- description: "Submit compact AlphaFold Protein Structure Database API requests for prediction, UniProt summary, sequence summary, and annotation lookups. Use when a user wants AlphaFold metadata or concise structure summaries"
- use when: Look up the AlphaFold DB predicted-model record, summary or annotations for a UniProt accession; metadata only, no structure analysis. For deposited experimental structures use rcsb-pdb-skill.

### bgee-skill
- id: life-science-research:bgee-skill (source path: plugins/life-science-research/skills/bgee-skill/SKILL.md)
- description: "Submit compact Bgee SPARQL requests for healthy wild-type expression metadata and ontology-aware lookup patterns. Use when a user wants concise Bgee summaries; save raw results only on request."
- use when: Query healthy wild-type, cross-species gene expression with anatomy/stage ontology awareness through Bgee SPARQL. Niche: you must author the query (only trivial ASK/SELECT examples ship). Human tissue/cell-line expression is human-protein-atlas-skill.
- needs: a SPARQL query or query file

### bindingdb-skill
- id: life-science-research:bindingdb-skill (source path: plugins/life-science-research/skills/bindingdb-skill/SKILL.md)
- description: "Submit compact BindingDB REST API requests for ligand-target binding lookups by PDB, UniProt, or similarity search. Use when a user wants concise BindingDB summaries; save raw payloads only on request."
- use when: Get measured ligand-target binding data by PDB ID or UniProt accession, similar ligands by SMILES, or targets of a compound. Broader bioactivity and mechanism of action is chembl-skill.
- needs: add response=application/json for structured output; an empty result can return an empty body

### biobankjapan-phewas-skill
- id: life-science-research:biobankjapan-phewas-skill (source path: plugins/life-science-research/skills/biobankjapan-phewas-skill/SKILL.md)
- description: "Fetch compact BioBank Japan PheWAS summaries for single variants by accepting rsID, GRCh38, or GRCh37 input and resolving to the required GRCh37 query. Use when a user wants concise BBJ association results for one variant"
- use when: List phenotype associations for ONE variant in the BioBank Japan (East Asian) cohort. Same shape as the other cohort PheWAS skills; choose by the cohort the user names. Resolves input to GRCh37.
- needs: exactly one of rsid/grch37/grch38/variant

### biorxiv-skill
- id: life-science-research:biorxiv-skill (source path: plugins/life-science-research/skills/biorxiv-skill/SKILL.md)
- description: "Submit compact bioRxiv and medRxiv API requests for details, publication-linkage, and DOI lookups. Use when a user wants concise preprint metadata summaries"
- use when: Fetch bioRxiv/medRxiv preprint metadata by date window or DOI, or check whether a preprint was later published. No keyword-search path; for PubMed search use ncbi-entrez-skill.

### biostudies-arrayexpress-skill
- id: life-science-research:biostudies-arrayexpress-skill (source path: plugins/life-science-research/skills/biostudies-arrayexpress-skill/SKILL.md)
- description: "Submit compact BioStudies and ArrayExpress API requests for free-text search and accession-based study retrieval. Use when a user wants concise BioStudies summaries"
- use when: Find or fetch functional-genomics/omics study records by free text or accession (for example E-MTAB). EBI study discovery only; single-cell collections are cellxgene-skill, ENCODE assays are encode-skill.

### cbioportal-skill
- id: life-science-research:cbioportal-skill (source path: plugins/life-science-research/skills/cbioportal-skill/SKILL.md)
- description: "Submit compact cBioPortal API requests for studies, molecular profiles, mutations, clinical data, and samples. Use when a user wants concise cBioPortal summaries"
- use when: Pull cancer-genomics cohort data: studies, molecular profiles, mutations in a gene, clinical data, samples. Cohort level; curated clinical interpretation of a cancer variant is civic-skill.
- needs: mutation fetches are POST requests

### cellxgene-skill
- id: life-science-research:cellxgene-skill (source path: plugins/life-science-research/skills/cellxgene-skill/SKILL.md)
- description: "Submit compact CELLxGENE Discover API requests for public collection and dataset metadata. Use when a user wants concise single-cell collection summaries"
- use when: Find public single-cell collection and dataset metadata in CZ CELLxGENE Discover; metadata, not expression values. Fetch one collection by ID rather than the full list.
- needs: the full collections list is large and needs a longer timeout

### chebi-skill
- id: life-science-research:chebi-skill (source path: plugins/life-science-research/skills/chebi-skill/SKILL.md)
- description: "Submit compact ChEBI 2.0 API requests for chemical search, compound lookup, ontology traversal, and structure metadata. Use when a user wants concise ChEBI summaries"
- use when: Search or fetch a ChEBI chemical-entity ontology record, including parent and child classes. Classification, not bioactivity (chembl-skill) or properties (pubchem-pug-skill).

### chembl-skill
- id: life-science-research:chembl-skill (source path: plugins/life-science-research/skills/chembl-skill/SKILL.md)
- description: "Submit compact ChEMBL API requests for activity, molecule, target, mechanism, and text-search endpoints. Use when a user wants concise ChEMBL summaries"
- use when: Get bioactivity, molecule, target and mechanism-of-action data from ChEMBL, or search molecules by text. The core drug-discovery source; measured binding by PDB/UniProt/SMILES is bindingdb-skill.

### civic-skill
- id: life-science-research:civic-skill (source path: plugins/life-science-research/skills/civic-skill/SKILL.md)
- description: "Submit compact CIViC GraphQL requests for cancer variant interpretation schema inspection and targeted evidence retrieval. Use when a user wants concise CIViC summaries"
- use when: Get clinical-interpretation evidence for cancer variants from CIViC. Supply a targeted GraphQL query; schema inspection is an option, not a required first step. Cohort mutation data is cbioportal-skill.
- needs: a GraphQL query or query file

### clinicaltrials-skill
- id: life-science-research:clinicaltrials-skill (source path: plugins/life-science-research/skills/clinicaltrials-skill/SKILL.md)
- description: "Submit compact ClinicalTrials.gov API v2 requests for study search, metadata, enums, search areas, and field statistics. Use when a user wants concise ClinicalTrials.gov summaries"
- use when: Search registered trials on ClinicalTrials.gov (for example recruiting trials for a condition) or read API enums and field statistics. The only trials source in this plugin; returns one page by default.

### clinvar-variation-skill
- id: life-science-research:clinvar-variation-skill (source path: plugins/life-science-research/skills/clinvar-variation-skill/SKILL.md)
- description: "Submit compact ClinVar Clinical Tables and NCBI Variation requests for search, VCV, RCV, SCV, and RefSNP lookups. Use when a user wants variant-level summaries or identifier mapping"
- use when: Look up the clinical significance of a variant: ClinVar search, VCV/RCV/SCV accession, or RefSNP (rs) record. Population frequency is gnomad-graphql-skill; coordinate mapping is ensembl-skill.
- needs: an action field (search, vcv, rcv, scv, refsnp) with its own required input

### efo-ontology-skill
- id: life-science-research:efo-ontology-skill (source path: plugins/life-science-research/skills/efo-ontology-skill/SKILL.md)
- description: "Submit compact EFO OLS4 requests for search, term lookup, children, and descendants. Use when a user wants concise EFO resolution or ontology-expansion summaries"
- use when: Resolve a disease or trait name to an EFO term, or expand it to children and descendants. Ontology resolution only; step 1 of locus-to-gene-mapper-skill.
- needs: term IRIs must be double-URL-encoded in term paths

### encode-skill
- id: life-science-research:encode-skill (source path: plugins/life-science-research/skills/encode-skill/SKILL.md)
- description: "Submit compact ENCODE REST API requests for object lookups, portal-style search, and metadata retrieval. Use when a user wants concise ENCODE summaries"
- use when: Find ENCODE consortium experiments, biosamples or an ENC accession object (for example RNA-seq experiments). Avoid large unfiltered searches.

### ensembl-skill
- id: life-science-research:ensembl-skill (source path: plugins/life-science-research/skills/ensembl-skill/SKILL.md)
- description: "Submit compact Ensembl REST API requests for lookup, overlap, cross-reference, and variation endpoints. Use when a user wants concise Ensembl summaries"
- use when: Look up a gene or transcript by Ensembl ID, features overlapping a region, cross-references, or variation by rsID. Identifier and coordinate mapping, not clinical meaning (clinvar-variation-skill).

### epigraphdb-skill
- id: life-science-research:epigraphdb-skill (source path: plugins/life-science-research/skills/epigraphdb-skill/SKILL.md)
- description: "Submit compact EpiGraphDB API requests for ontology, literature, MR, gene-drug, and support-path evidence. Use when a user wants concise EpiGraphDB summaries"
- use when: Query EpiGraphDB graph evidence: Mendelian randomization, GWAS-to-EFO mapping, gene-drug links, druggability PPI, literature triples. Niche; check ping/builds/meta endpoints first when availability matters.

### eqtl-catalogue-skill
- id: life-science-research:eqtl-catalogue-skill (source path: plugins/life-science-research/skills/eqtl-catalogue-skill/SKILL.md)
- description: "Submit compact eQTL Catalogue API requests for association retrieval and documented metadata endpoints. Use when a user wants concise public eQTL Catalogue summaries"
- use when: Get eQTL associations across uniformly reprocessed studies for a gene and/or variant, or list studies. GTEx-only, variant-keyed eQTLs are gtex-eqtl-skill. The upstream API is intermittently failing (400/500/timeouts); errors are reported verbatim.

### eva-skill
- id: life-science-research:eva-skill (source path: plugins/life-science-research/skills/eva-skill/SKILL.md)
- description: "Submit compact EVA REST requests for species metadata and archived variant lookups. Use when a user wants concise European Variation Archive summaries"
- use when: Look up European Variation Archive records: species list or an archived variant (for example rs699). Niche; clinical assertions are clinvar-variation-skill.

### finngen-phewas-skill
- id: life-science-research:finngen-phewas-skill (source path: plugins/life-science-research/skills/finngen-phewas-skill/SKILL.md)
- description: "Fetch compact FinnGen PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise FinnGen association results for one variant"
- use when: List phenotype associations for ONE variant in FinnGen (Finnish biobank). Same shape as the other cohort PheWAS skills; choose by the cohort the user names. Resolves input to GRCh38.
- needs: exactly one of rsid/grch37/grch38/variant

### genebass-gene-burden-skill
- id: life-science-research:genebass-gene-burden-skill (source path: plugins/life-science-research/skills/genebass-gene-burden-skill/SKILL.md)
- description: "Submit compact Genebass gene burden requests for one Ensembl gene ID and one burden set. Use when a user wants concise Genebass PheWAS summaries"
- use when: Get gene-level rare-variant burden phenotype associations (UK Biobank exomes) for one gene. Gene-level, unlike the variant-level PheWAS skills; step 6 of locus-to-gene-mapper-skill.
- needs: one Ensembl gene ID and one burden set (pLoF, missense|LC, synonymous) per call

### gnomad-graphql-skill
- id: life-science-research:gnomad-graphql-skill (source path: plugins/life-science-research/skills/gnomad-graphql-skill/SKILL.md)
- description: "Submit compact gnomAD GraphQL requests for frequency, gene constraint, and variant context queries. Use when a user wants concise gnomAD summaries"
- use when: Get population allele frequency, gene constraint, or variant consequence context from gnomAD. You write the GraphQL query (dataset such as gnomad_r4). Clinical assertions are clinvar-variation-skill.
- needs: a GraphQL query or query file

### gtex-eqtl-skill
- id: life-science-research:gtex-eqtl-skill (source path: plugins/life-science-research/skills/gtex-eqtl-skill/SKILL.md)
- description: "Fetch GTEx single-tissue eQTL associations from one variant input by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query for the GTEx v2 API. Use when a user wants eQTL associations returned as JSON."
- use when: Get GTEx single-tissue eQTLs for ONE variant. Returns a single JSON object, not a markdown summary, and has no save_raw. Multi-study eQTLs by gene are eqtl-catalogue-skill; step 5 of locus-to-gene-mapper-skill.
- needs: Python requests; exactly one of rsid/grch37/grch38/variant (resolved to GRCh38)

### gwas-catalog-skill
- id: life-science-research:gwas-catalog-skill (source path: plugins/life-science-research/skills/gwas-catalog-skill/SKILL.md)
- description: "Submit compact GWAS Catalog REST API v2 requests for studies, associations, SNPs, EFO traits, genes, publications, loci, and metadata. Use when a user wants concise GWAS Catalog summaries"
- use when: Query curated published GWAS: studies, associations, SNPs, EFO traits, genes, publications, loci. Integrated target/disease evidence is opentargets-skill; step 2 of locus-to-gene-mapper-skill.

### hmdb-skill
- id: life-science-research:hmdb-skill (source path: plugins/life-science-research/skills/hmdb-skill/SKILL.md)
- description: "Submit compact HMDB search requests for metabolites, proteins, diseases, and pathways. Use when a user wants concise HMDB summaries"
- use when: Search the Human Metabolome Database for metabolites, proteins, diseases or pathways (one category per request). Chemical classification is chebi-skill; compound properties are pubchem-pug-skill.

### human-protein-atlas-skill
- id: life-science-research:human-protein-atlas-skill (source path: plugins/life-science-research/skills/human-protein-atlas-skill/SKILL.md)
- description: "Submit compact Human Protein Atlas requests for gene JSON, search downloads, and page-level tissue or cell-line lookups. Use when a user wants concise Human Protein Atlas summaries; save raw JSON or HTML only on request."
- use when: Find where a gene is expressed in human tissues or cell lines using Human Protein Atlas pages and downloads. Tissue-plausibility evidence, not causal-gene selection; optional last step of locus-to-gene-mapper-skill.
- needs: an ENSG ID for gene JSON, a gene symbol for tissue/cell-line pages, or search terms for search downloads

### ipd-skill
- id: life-science-research:ipd-skill (source path: plugins/life-science-research/skills/ipd-skill/SKILL.md)
- description: "Submit compact IPD REST requests for HLA allele and cell-level metadata using the public IPD query API. Use when a user wants concise IPD summaries; save raw JSON or text only on request."
- use when: Look up IPD HLA alleles (for example alleles matching A*01) or IPD cell metadata. Niche immunogenetics source; use project=HLA for HLA browsing.

### locus-to-gene-mapper-skill
- id: life-science-research:locus-to-gene-mapper-skill (source path: plugins/life-science-research/skills/locus-to-gene-mapper-skill/SKILL.md)
- description: "Map GWAS loci to ranked candidate genes using a deterministic multi-skill chain (EFO -> GWAS -> coordinates -> Open Targets L2G/coloc -> eQTL -> burden/coding context), with reproducible tables and optional figures. Use when a user provides a trait/EFO term and/or lead variants and needs locus-to-gene prioritization for downstream biology decisions."
- use when: Rank candidate genes at GWAS signals from a trait, EFO ID or lead rsIDs, with reproducible multi-source scoring and provenance. Not a single association lookup (gwas-catalog-skill) and not fine-mapping; the router sends standard locus-to-gene work here.
- needs: at least one of trait_query/efo_id/seed_rsids; Python 3.11+, requests, writable output path; matplotlib/seaborn/pandas for figures
- side effects: writes locus_to_gene_mapping.json and locus_to_gene_summary.md (default ./output/); figures only if enabled (default on for trait-only runs)
- part of: entry point of a fixed 9-step chain: efo-ontology-skill, gwas-catalog-skill, RefSNP coordinates, opentargets-skill, gtex-eqtl-skill, genebass-gene-burden-skill, then optional clinvar-variation-skill, gnomad-graphql-skill, human-protein-atlas-skill (flags default on); no retrieval after scoring starts; stops at candidate prioritization, not causality

### metabolights-skill
- id: life-science-research:metabolights-skill (source path: plugins/life-science-research/skills/metabolights-skill/SKILL.md)
- description: "Submit compact MetaboLights requests for study discovery and study-level metabolomics metadata. Use when a user wants concise MetaboLights summaries"
- use when: Find public metabolomics studies or summarize one study (MTBLS accession). Study deposits only; compound facts are pubchem-pug-skill, chebi-skill or hmdb-skill.

### mgnify-skill
- id: life-science-research:mgnify-skill (source path: plugins/life-science-research/skills/mgnify-skill/SKILL.md)
- description: "Submit compact MGnify API requests for microbiome studies, samples, and biome metadata. Use when a user wants concise MGnify summaries"
- use when: Find microbiome studies, samples or biomes, or look up an MGnify accession. Archive metadata, not a metagenomic computation or sequence analysis.

### ncbi-blast-skill
- id: life-science-research:ncbi-blast-skill (source path: plugins/life-science-research/skills/ncbi-blast-skill/SKILL.md)
- description: "Submit, poll, and summarize NCBI BLAST Common URL API jobs (Blast.cgi) for nucleotide or protein sequences. Use when a user wants RID status, BLAST results, or compact top-hit summaries; fetch raw Text/JSON2 only on request."
- use when: Run or follow a BLAST similarity search for a FASTA query, check a BLAST RID's status, or show top hits. Computes similarity; retrieving a known record is ncbi-entrez-skill or uniprot-skill.
- needs: Python requests; action submit/run requires program (blastn/blastp/blastx/tblastn/tblastx), database, query FASTA and email or NCBI_EMAIL; status/fetch requires RID; at least 10 s between requests and 60 s between polls of one RID
- side effects: submit/run uploads the query sequence to NCBI and creates a remote compute job; always surfaces the RID so it can be resumed. Raw output writes only on request (default /tmp/ncbi-blast-<rid>.<json|txt>); the source directs installing requests if missing.

### ncbi-clinicaltables-skill
- id: life-science-research:ncbi-clinicaltables-skill (source path: plugins/life-science-research/skills/ncbi-clinicaltables-skill/SKILL.md)
- description: "Submit compact Clinical Tables NCBI Gene requests for human gene lookup, pagination, and field selection. Use when a user wants concise autocomplete-style human gene search results"
- use when: Autocomplete or resolve human gene search text to GeneID and symbol, with field selection. Search rows only; a full Gene record is ncbi-entrez-skill.

### ncbi-datasets-skill
- id: life-science-research:ncbi-datasets-skill (source path: plugins/life-science-research/skills/ncbi-datasets-skill/SKILL.md)
- description: "Submit compact NCBI Datasets v2 requests for assembly, genome, taxonomy, and related metadata endpoints. Use when a user wants concise NCBI Datasets summaries; save raw JSON or text only on request."
- use when: Get NCBI Datasets v2 assembly reports, genome metadata by taxon, or taxonomy (for example GCF_000001405.40, taxon 9606). Metadata, not a genome download.

### ncbi-entrez-skill
- id: life-science-research:ncbi-entrez-skill (source path: plugins/life-science-research/skills/ncbi-entrez-skill/SKILL.md)
- description: "Submit compact NCBI Entrez E-Utilities requests for PubMed, Gene, Protein, Nucleotide, PMC metadata, and GEO metadata workflows. Use when a user wants concise Entrez search, fetch, summary, or link results; save raw JSON or XML only on request."
- use when: Search PubMed; fetch Gene, Protein or Nucleotide records; get PMC metadata; find GEO series and linked papers; follow links between NCBI records. GEO yields metadata, not expression matrices. It hands off BLAST to ncbi-blast-skill, PMC Open Access to ncbi-pmc-skill and Datasets v2 to ncbi-datasets-skill.
- needs: endpoint (esearch/esummary/efetch/elink/einfo) plus params

### ncbi-pmc-skill
- id: life-science-research:ncbi-pmc-skill (source path: plugins/life-science-research/skills/ncbi-pmc-skill/SKILL.md)
- description: "Submit compact NCBI PMC Open Access requests for article/file availability metadata. Use when a user wants concise PMC Open Access summaries; save raw XML only on request."
- use when: Check whether a PMCID (or supported DOI) is in PMC Open Access and which files exist. Only the OA service, despite the name; not full text or article synthesis. PubMed search is ncbi-entrez-skill.

### opentargets-skill
- id: life-science-research:opentargets-skill (source path: plugins/life-science-research/skills/opentargets-skill/SKILL.md)
- description: "Submit compact Open Targets Platform GraphQL requests for target, disease, drug, variant, study, and search data, including associated-disease datasource heatmap matrices. Use when a user wants concise Open Targets summaries or per-datasource evidence context"
- use when: Get Open Targets Platform evidence for a target, disease, drug, variant or study, including credible sets, L2G, colocalisation and a disease-by-datasource matrix. You write the GraphQL query; datasource scores show evidence breadth, not causality. Step 4 of locus-to-gene-mapper-skill.
- needs: a GraphQL query or query file; the matrix helper needs an Ensembl target ID

### pharmgkb-skill
- id: life-science-research:pharmgkb-skill (source path: plugins/life-science-research/skills/pharmgkb-skill/SKILL.md)
- description: "Submit compact PharmGKB API requests for genes, variants, clinical annotations, dosing guidelines, and search. Use when a user wants concise PharmGKB summaries"
- use when: Find pharmacogenomic gene/variant records, clinical annotations or dosing guidelines for a drug, gene or variant (or a PA identifier). Source records only; no personalized prescribing workflow.

### pride-skill
- id: life-science-research:pride-skill (source path: plugins/life-science-research/skills/pride-skill/SKILL.md)
- description: "Submit compact PRIDE Archive API requests for proteomics project discovery and project-level metadata. Use when a user wants concise PRIDE summaries"
- use when: Find proteomics projects by topic or summarize one PRIDE project (PXD accession). Project level; granular peptide/PSM/spectrum objects are proteomexchange-skill.

### proteomexchange-skill
- id: life-science-research:proteomexchange-skill (source path: plugins/life-science-research/skills/proteomexchange-skill/SKILL.md)
- description: "Submit compact ProteomeXchange PROXI requests for datasets, libraries, peptidoforms, proteins, PSMs, spectra, and USI examples. Use when a user wants concise PROXI summaries"
- use when: Look up granular proteomics objects through PROXI: datasets, libraries, peptidoforms, proteins, PSMs, spectra, USI examples. Object level, where pride-skill is project level.

### pubchem-pug-skill
- id: life-science-research:pubchem-pug-skill (source path: plugins/life-science-research/skills/pubchem-pug-skill/SKILL.md)
- description: "Submit compact PubChem PUG REST requests for compound properties, descriptions, assay summaries, and substance metadata. Use when a user wants concise PubChem summaries"
- use when: Get compound properties (formula, weight), descriptions, assay summaries or substance metadata from PubChem. Chemical identity and properties; bioactivity is chembl-skill, classification is chebi-skill.

### quickgo-skill
- id: life-science-research:quickgo-skill (source path: plugins/life-science-research/skills/quickgo-skill/SKILL.md)
- description: "Submit compact QuickGO requests for GO terms, annotations, and ontology traversal. Use when a user wants concise QuickGO summaries"
- use when: Explain a GO term and its parents/children, or fetch GO annotations for a gene product. annotation/search is upstream-fragile: on failure fall back to ontology lookup or uniprot-skill GO annotations and say so; an empty result is not missing biology.

### rcsb-pdb-skill
- id: life-science-research:rcsb-pdb-skill (source path: plugins/life-science-research/skills/rcsb-pdb-skill/SKILL.md)
- description: "Submit compact RCSB PDB requests for core metadata, Search API queries, and FASTA downloads. Use when a user wants concise RCSB summaries; save raw JSON or FASTA only on request."
- use when: Summarize a PDB entry or assembly (for example 4HHB), search PDB entries, or fetch an entry's FASTA. Deposited experimental structures; predicted models are alphafold-skill. No modelling.

### reactome-skill
- id: life-science-research:reactome-skill (source path: plugins/life-science-research/skills/reactome-skill/SKILL.md)
- description: "Submit compact Reactome ContentService requests for pathway, event, participant, search, and diagram-related data. Use when a user wants concise Reactome summaries"
- use when: Find pathways containing a protein, participants of a Reactome event, or pathway/event data (for example R-HSA-199420). Pathway membership; reaction level is rhea-skill, network enrichment is string-skill.

### research-router-skill
- id: life-science-research:research-router-skill (source path: plugins/life-science-research/skills/research-router-skill/SKILL.md)
- description: "Route broad or ambiguous life-sciences research requests to the right skills, normalize core entities, optionally parallelize independent evidence gathering with subagents when available, and synthesize a concise evidence-backed answer. Use when a user asks a general life-sciences question that could span multiple sources or analysis types."
- use when: Entry router for broad, mixed or unclear life-science questions (for example what is known about IL6R and asthma). Classify into 1-3 lanes, normalize entities first, pick the minimum downstream skills, gather evidence, then synthesize. Not for a narrow single-source lookup: go straight to that skill.
- needs: optional Codex subagents only for independent lanes; no script or connector of its own
- part of: entry router for life-science-research. Sequence: understand objective -> normalize entities -> select minimum skills -> gather evidence -> synthesize (direct answer, evidence by lane, caveats, next analyses). Hands standard locus-to-gene work to locus-to-gene-mapper-skill; never overstates causality from association

### rhea-skill
- id: life-science-research:rhea-skill (source path: plugins/life-science-research/skills/rhea-skill/SKILL.md)
- description: "Submit compact Rhea reaction search requests for biochemical reactions and reaction IDs. Use when a user wants concise Rhea summaries"
- use when: Find biochemical reactions by compound, EC number or Rhea ID (for example RHEA:47148). Niche, reaction level; pathway level is reactome-skill.

### rnacentral-skill
- id: life-science-research:rnacentral-skill (source path: plugins/life-science-research/skills/rnacentral-skill/SKILL.md)
- description: "Submit compact RNAcentral API requests for RNA entry browsing, single-entry lookup, and cross-reference retrieval. Use when a user wants concise RNAcentral summaries"
- use when: Resolve an RNAcentral URS accession and species, fetch its cross-references, or search RNA entries. Niche; keep collection paths targeted (rna/<URS>/<taxid>), broad rna/ can time out.

### string-skill
- id: life-science-research:string-skill (source path: plugins/life-science-research/skills/string-skill/SKILL.md)
- description: "Submit compact STRING API requests for network, interaction partner, and enrichment endpoints. Use when a user wants concise STRING summaries"
- use when: Find interaction partners for a protein, build a network for a protein list, or run enrichment on an identifier list with STRING. No graph rendering; curated pathway membership is reactome-skill.
- needs: a stable caller_identity (a request identifier, not a credential); POST with form_body

### tpmi-phewas-skill
- id: life-science-research:tpmi-phewas-skill (source path: plugins/life-science-research/skills/tpmi-phewas-skill/SKILL.md)
- description: "Fetch compact TPMI PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise TPMI association results for one variant"
- use when: List phenotype associations for ONE variant in TPMI. Same shape as the other cohort PheWAS skills; choose by the cohort the user names. Resolves input to GRCh38.
- needs: exactly one of rsid/grch37/grch38/variant

### ukb-topmed-phewas-skill
- id: life-science-research:ukb-topmed-phewas-skill (source path: plugins/life-science-research/skills/ukb-topmed-phewas-skill/SKILL.md)
- description: "Fetch compact UKB-TOPMed PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise UKB-TOPMed association results for one variant"
- use when: List phenotype associations for ONE variant in UKB-TOPMed. Same shape as the other cohort PheWAS skills; choose by the cohort the user names. Resolves input to GRCh38.
- needs: exactly one of rsid/grch37/grch38/variant

### uniprot-skill
- id: life-science-research:uniprot-skill (source path: plugins/life-science-research/skills/uniprot-skill/SKILL.md)
- description: "Submit compact UniProt REST API requests for UniProtKB, UniRef, UniParc, and FASTA stream endpoints. Use when a user wants concise UniProt summaries; save raw JSON or FASTA only on request."
- use when: Find a protein accession (for example human TP53), summarize one, look up UniRef/UniParc records, or fetch FASTA. Protein knowledge and sequence; computed similarity is ncbi-blast-skill, PDB entries are rcsb-pdb-skill.

## Family: ngs-analysis
- source path: `plugins/ngs-analysis` (v1.0.3)
- manifest notes: Codex-only manifest; no MCP server, app connector or hooks; MIT; category Education & Research. Ships Python runners, `references/*.json` registries and workflows that skills call as `python plugins/ngs-analysis/scripts/<name>.py` from the repo root, so a host that installs the plugin elsewhere needs those paths adjusted. Nothing is installed without approval: preflight writes `install_plan.json` and `install_commands.sh` for review (the script runs only with `NGS_RUN_INSTALL_COMMANDS=1` after explicit approval); never modify system Python (use conda/mamba or containers); `bcl-convert` and 10x Cell Ranger are licensed and never auto-downloaded; ask before cloud upload of human data; clinical interpretation is out of scope. Runners write a run envelope and validate/dry-run unless `--execute`.
- router: `ngs-analysis-router` covers BCL, FASTQ, BAM/CRAM, count-matrix and VCF requests. Inspect the inputs, ask only the missing questions (assay, organism/reference, paired/single-end, design, installs allowed), route to ONE leaf, run preflight (`--emit-install-plan`), and return a six-part output; it stops before executing the assay. Four dispatchers hand to leaves: `ngs-dna-variant-calling`, `ngs-bulk-rnaseq`, `ngs-scrna-seq`, `ngs-epigenomics-peaks`.
- development distance: far (genomics/bioinformatics pipelines)
- disclosure: router-delegated. The router and four dispatchers choose the leaf, so records stay one-liners.

### ngs-analysis-router
- id: ngs-analysis:ngs-analysis-router (source path: plugins/ngs-analysis/skills/ngs-analysis-router/SKILL.md)
- description: "Route BCL, FASTQ, BAM/CRAM, count-matrix, or VCF sequencing requests to the right public NGS analysis skill and ask only the missing assay-specific setup questions."
- use when: I have sequencing files (BCL, FASTQ, BAM/CRAM, count matrix, VCF) and have not named the assay; it inspects inputs, routes to one leaf and runs a preflight.
- side effects: writes `install_plan.json` and `install_commands.sh` for review only; executes no assay.

### ngs-runtime-env
- id: ngs-analysis:ngs-runtime-env (source path: plugins/ngs-analysis/skills/ngs-runtime-env/SKILL.md)
- description: "Check whether public NGS tools and packages already exist before downloading, installing, or running a sequencing pipeline."
- use when: Is tool X already installed? What do I need for pipeline Y? Are reference or database bundles present?
- side effects: writes plan and inventory artifacts; installs only on explicit request.

### ngs-bcl-to-fastq
- id: ngs-analysis:ngs-bcl-to-fastq (source path: plugins/ngs-analysis/skills/ngs-bcl-to-fastq/SKILL.md)
- description: "Validate Illumina BCL run folders and sample sheets, plan demultiplexing, review index/UMI/lane choices, run BCL-to-FASTQ conversion, and interpret demux metrics while surfacing license/download boundaries."
- use when: I have an Illumina BCL run folder and sample sheet and want FASTQs or a validated run.
- needs: `bcl-convert` (or `bcl2fastq`) already installed; never auto-downloaded.

### ngs-fastq-qc
- id: ngs-analysis:ngs-fastq-qc (source path: plugins/ngs-analysis/skills/ngs-fastq-qc/SKILL.md)
- description: "Validate FASTQ inputs, run local FastQC/MultiQC QC, interpret QC signals, and optionally execute fastp or Cutadapt trimming branches without overwriting raw reads."
- use when: I have FASTQs and want QC only, a trimming decision, or help reading FastQC/MultiQC output.

### ngs-dna-variant-calling
- id: ngs-analysis:ngs-dna-variant-calling (source path: plugins/ngs-analysis/skills/ngs-dna-variant-calling/SKILL.md)
- description: "Dispatch WGS, WES, or targeted DNA variant requests to germline, somatic, or UMI-panel skills, then plan public nf-core/sarek, GATK4, DeepVariant, samtools, or bcftools workflows."
- use when: WGS/WES/panel variant calling where the sample model is not decided; dispatches to the germline, somatic or UMI-panel skill.

### ngs-dna-germline-variants
- id: ngs-analysis:ngs-dna-germline-variants (source path: plugins/ngs-analysis/skills/ngs-dna-germline-variants/SKILL.md)
- description: "Run or plan deep germline WGS, WES, targeted-panel, cohort, or trio variant-calling workflows with reference-build, known-sites, QC, joint-calling, and annotation checks."
- use when: Inherited-variant calls for WGS, WES, panel, cohort, family or trio data.

### ngs-dna-somatic-variants
- id: ngs-analysis:ngs-dna-somatic-variants (source path: plugins/ngs-analysis/skills/ngs-dna-somatic-variants/SKILL.md)
- description: "Run or plan tumor-normal, tumor-only, WGS, WES, or cancer-panel somatic variant workflows with pairing, contamination, panel-of-normals, purity, QC, and annotation checks."
- use when: Tumor-normal or tumor-only cancer variant calling.

### ngs-dna-umi-panel-variants
- id: ngs-analysis:ngs-dna-umi-panel-variants (source path: plugins/ngs-analysis/skills/ngs-dna-umi-panel-variants/SKILL.md)
- description: "Run or plan targeted DNA panel variant workflows that use UMIs, duplex consensus reads, molecular barcodes, low-frequency calling, target coverage, and panel-specific QC."
- use when: A targeted panel with UMIs, duplex consensus or molecular barcodes where low-allele-fraction calls matter.

### ngs-bulk-rnaseq
- id: ngs-analysis:ngs-bulk-rnaseq (source path: plugins/ngs-analysis/skills/ngs-bulk-rnaseq/SKILL.md)
- description: "Dispatch bulk RNA-seq requests to FASTQ-to-count QC or count-matrix differential-expression skills using nf-core/rnaseq, STAR, Salmon, featureCounts, MultiQC, and R/Bioconductor workflows."
- use when: Bulk RNA-seq where it is unclear whether I need FASTQ-to-counts, differential expression or both; dispatches.

### ngs-bulk-rnaseq-counts-qc
- id: ngs-analysis:ngs-bulk-rnaseq-counts-qc (source path: plugins/ngs-analysis/skills/ngs-bulk-rnaseq-counts-qc/SKILL.md)
- description: "Run or plan bulk RNA-seq FASTQ-to-count processing with sample-sheet, strandedness, genome annotation, alignment or pseudoalignment, MultiQC, and count-matrix QC checks."
- use when: I have bulk RNA-seq FASTQs or aligned reads and want a count matrix with QC.

### ngs-bulk-rnaseq-differential-expression
- id: ngs-analysis:ngs-bulk-rnaseq-differential-expression (source path: plugins/ngs-analysis/skills/ngs-bulk-rnaseq-differential-expression/SKILL.md)
- description: "Run or plan bulk RNA-seq differential-expression analysis from count matrices with replicate, design formula, contrast, batch, normalization, QC plot, and result-table checks."
- use when: I have a count matrix plus sample metadata and want contrasts, DE tables and QC plots.
- side effects: launches a localhost Marimo review app.

### ngs-scrna-seq
- id: ngs-analysis:ngs-scrna-seq (source path: plugins/ngs-analysis/skills/ngs-scrna-seq/SKILL.md)
- description: "Route single-cell or single-nucleus RNA-seq FASTQs to public count-generation workflows and defer post-count matrix QC, annotation, clustering, and UMAP analysis to the embedded scrna-seq-qc skill."
- use when: Single-cell or single-nucleus RNA-seq FASTQs needing count generation; post-count QC, clustering and UMAP go to `scrna-seq-qc`.
- needs: Cell Ranger only with the 10x EULA accepted.

### scrna-seq-qc
- id: ngs-analysis:scrna-seq-qc (source path: plugins/ngs-analysis/skills/scrna-seq-qc/SKILL.md)
- description: "Process, quality-control, annotate, and visualize single-cell or single-nucleus RNA-seq datasets across tissues and species. Use when Codex needs to build, adapt, or review a general scRNA-seq QC pipeline; choose dataset-appropriate cell-level filters from QC distributions; run required scDblFinder-based doublet and ambient-RNA filtering; annotate cells with matched references or marker-based fallbacks; or generate global and per-group UMAP visualizations for large scRNA-seq datasets."
- use when: I have a scRNA count matrix, `.h5ad`, `.rds` or Cell Ranger output and want QC thresholds, doublet/ambient removal, annotation, clustering and UMAPs.
- side effects: its runner auto-launches a localhost Marimo review app.

### ngs-epigenomics-peaks
- id: ngs-analysis:ngs-epigenomics-peaks (source path: plugins/ngs-analysis/skills/ngs-epigenomics-peaks/SKILL.md)
- description: "Dispatch ATAC-seq, ChIP-seq, CUT&RUN, or CUT&Tag requests to assay-specific QC, alignment, signal-track, peak-calling, consensus, and differential peak workflows."
- use when: ATAC-seq, ChIP-seq, CUT&RUN or CUT&Tag where the assay-specific skill is not chosen; dispatches.

### ngs-atacseq-peaks-qc
- id: ngs-analysis:ngs-atacseq-peaks-qc (source path: plugins/ngs-analysis/skills/ngs-atacseq-peaks-qc/SKILL.md)
- description: "Run or plan ATAC-seq QC, alignment, TSS enrichment, fragment-size, blacklist, peak-calling, consensus peak, and differential accessibility workflows."
- use when: ATAC-seq FASTQ or BAM: accessibility QC, peaks, consensus peaks, differential accessibility.

### ngs-chip-cutrun-peaks-qc
- id: ngs-analysis:ngs-chip-cutrun-peaks-qc (source path: plugins/ngs-analysis/skills/ngs-chip-cutrun-peaks-qc/SKILL.md)
- description: "Run or plan ChIP-seq, CUT&RUN, or CUT&Tag QC, control handling, spike-in, peak calling, broad-vs-narrow target selection, replicate, bigWig, and differential binding workflows."
- use when: ChIP-seq, CUT&RUN or CUT&Tag with controls and a target (transcription factor or histone mark).

### ngs-amplicon-microbiome
- id: ngs-analysis:ngs-amplicon-microbiome (source path: plugins/ngs-analysis/skills/ngs-amplicon-microbiome/SKILL.md)
- description: "Kick off public 16S, 18S, ITS, COI, or other marker-gene amplicon microbiome workflows using nf-core/ampliseq, QIIME2, DADA2, and Cutadapt."
- use when: 16S, 18S, ITS or COI marker-gene FASTQs needing ASVs, taxonomy and diversity.
- needs: primers with orientation, a versioned taxonomy database and metadata; without them it reports a read-QC readiness bundle only.

### ngs-shotgun-metagenomics
- id: ngs-analysis:ngs-shotgun-metagenomics (source path: plugins/ngs-analysis/skills/ngs-shotgun-metagenomics/SKILL.md)
- description: "Kick off public shotgun metagenomics QC, host-depletion, taxonomic profiling, and functional profiling workflows using nf-core/taxprofiler, Kraken2, Bracken, MetaPhlAn, and HUMAnN."
- use when: Shotgun metagenomic FASTQs needing QC, host depletion, and taxonomic or functional profiles.
- needs: databases for the selected profiling backend; Bracken/HUMAnN bundles become blocking only when their branches are requested; supplying `--host-reference` to the backend runner makes KneadData required.

## Family: boltz-api-cli
- source path: `plugins/boltz-api-cli` (v0.1.1, author Boltz, MIT; upstream `https://github.com/boltz-bio/boltz-api-skills`)
- manifest notes: Codex manifest only (category Scientific Research); no MCP server, app connector, hooks or commands. Wraps the external `boltz-api` Go CLI. Auth is `boltz-api auth login --device-code` or a provisioned `BOLTZ_API_KEY` (never pasted in chat). Jobs spend real money: every job skill runs `estimate-cost`, shows USD and waits for explicit confirmation before submission (`run` for ADME, `start` for the other job skills). Install needs explicit confirmation of the exact command (see `boltz-cli-setup`). Skills name both Claude Code and Codex conventions for background downloads.
- router: none. `boltz-cli-setup` is the shared prerequisite (every job skill sends the user there when the CLI is missing, auth fails or the sandbox blocks); `boltz-check-status` is the shared recovery skill for existing jobs.
- development distance: far (science)
- disclosure: simple. Eight skills in a domain far from software development; short records.

### boltz-check-status
- id: boltz-api-cli:boltz-check-status (source path: plugins/boltz-api-cli/skills/boltz-check-status/SKILL.md)
- description: "Boltz job status and result recovery. Use when listing jobs, checking progress, resuming downloads, recovering results, or downloading an existing job ID. Not for starting new jobs."
- use when: Inspect an existing Boltz job: list jobs, check progress, resume a download, recover results by job ID. Never reruns `start`.
- needs: `boltz-api` authenticated for remote queries/downloads; a run name/directory for local `download-status`.
- side effects: downloads recovered artifacts to the local run directory; no new paid job. ADME recovery reads `retrieve` or local `run.json`, with no download step.

### boltz-cli-setup
- id: boltz-api-cli:boltz-cli-setup (source path: plugins/boltz-api-cli/skills/boltz-cli-setup/SKILL.md)
- description: "Boltz CLI setup and auth. Use when installing, updating, verifying, or authenticating `boltz-api`, or fixing missing CLI, PATH, sandbox, browser login, or auth errors."
- use when: `boltz-api` is missing, outdated, unauthenticated or sandbox-blocked; prerequisite for every other Boltz skill.
- needs: Network to `install.boltz.bio`, a browser for device-code login, possibly a sandbox bypass.
- side effects: installs a CLI only after the user confirms the exact command; starts device-code login without asking.

### boltz-protein-design
- id: boltz-api-cli:boltz-protein-design (source path: plugins/boltz-api-cli/skills/boltz-protein-design/SKILL.md)
- description: "Design new protein binders with Boltz. Use when generating protein, peptide, antibody, nanobody, or custom binder candidates for a target. Not for screening existing proteins or small molecules."
- use when: Generate new protein, peptide, antibody or nanobody binders for a target; for a new target the first move is a choice of target exploration versus direct design.
- needs: `boltz-api` authenticated; target as CIF/PDB or sequence.
- side effects: spends real money (default 50,000-design tier); fresh "go" before every `start`.

### boltz-protein-screen
- id: boltz-api-cli:boltz-protein-screen (source path: plugins/boltz-api-cli/skills/boltz-protein-screen/SKILL.md)
- description: "Screen existing protein binders with Boltz. Use when ranking a supplied protein, peptide, antibody, nanobody, or binder library against a target. Not for designing new proteins or screening small molecules."
- use when: Rank a supplied library of proteins, peptides, antibodies or nanobodies against a target.
- needs: `boltz-api` authenticated; candidates and target.
- side effects: spends real money; confirm the `estimate-cost` figure first.

### boltz-small-molecule-adme
- id: boltz-api-cli:boltz-small-molecule-adme (source path: plugins/boltz-api-cli/skills/boltz-small-molecule-adme/SKILL.md)
- description: "Predict Tier-1 ADME/ADMET for small molecules with Boltz from bare SMILES — no target, no docking. Use when the user wants solubility, permeability, or lipophilicity/logD for a molecule or list of molecules. Not for ranking molecules against a protein target (use boltz-small-molecule-screen, which already returns ADME free)."
- use when: Solubility, permeability or lipophilicity for SMILES with no protein target; with a target use `boltz-small-molecule-screen`, which returns ADME free.
- needs: `boltz-api` authenticated; at most 128 molecules per request.
- side effects: spends real money (source rate $0.01 per molecule; quote `estimate-cost` and obtain explicit confirmation before `run`); synchronous, writes local results with no separate download step.

### boltz-small-molecule-design
- id: boltz-api-cli:boltz-small-molecule-design (source path: plugins/boltz-api-cli/skills/boltz-small-molecule-design/SKILL.md)
- description: "Design new small-molecule binders with Boltz. Use when generating novel ligands or hits for a target without a fixed compound library. Not for screening existing molecules or one-off docking."
- use when: Generate novel small-molecule hits for a protein target when there is no compound library.
- needs: `boltz-api` authenticated; target sequence, optional pocket residues.
- side effects: spends real money ($0.025 per molecule, 10 to 1,000,000).

### boltz-small-molecule-screen
- id: boltz-api-cli:boltz-small-molecule-screen (source path: plugins/boltz-api-cli/skills/boltz-small-molecule-screen/SKILL.md)
- description: "Screen existing small-molecule libraries with Boltz. Use when docking, scoring, or ranking a supplied SMILES or compound library against a target; also returns free Tier-1 ADME/ADMET (solubility, permeability, lipophilicity/logD) per molecule. Not for de novo molecule design, one-off docking, or ADME on bare SMILES with no target (use boltz-small-molecule-adme)."
- use when: Dock, score and rank a supplied SMILES library against a protein target; each hit includes a free ADME block.
- needs: `boltz-api` authenticated; library and target.
- side effects: spends real money ($0.025 per molecule).

### boltz-structure-and-binding
- id: boltz-api-cli:boltz-structure-and-binding (source path: plugins/boltz-api-cli/skills/boltz-structure-and-binding/SKILL.md)
- description: "Predict structures and binding for one defined complex with Boltz. Use when folding a protein, RNA, DNA, or ligand complex, docking one ligand, predicting an interface, or scoring binding. Not for screening libraries or design."
- use when: Fold or dock one defined complex (protein, RNA, DNA, ligand) and score binding; not for libraries or design.
- needs: `boltz-api` authenticated; read the skill's `references/api.md` before the first payload.
- side effects: spends real money; no published rate, quote only the `estimate-cost` figure.

## Family: zotero
- source path: `plugins/zotero` (v0.1.2)
- manifest notes: Codex manifest only; no MCP server, app connector or hooks. MIT; category Education & Research. A standard-library Python 3 helper talks to Zotero Desktop's local API (`http://127.0.0.1:23119`, no API key for reads); imports go through Zotero's own connector endpoint. No cloud account or payment.
- router: none (single skill; internal order is status check -> enable if asked -> requested operation)
- development distance: far (reference management; touches LaTeX/Markdown drafts and `.bib` files)
- disclosure: simple. One skill, so a single short record suffices.

### Zotero
- id: zotero:zotero (source path: plugins/zotero/skills/zotero/SKILL.md)
- description: "Use Zotero Desktop from Codex to enable/probe the local API, search a local Zotero library, list items/collections/tags, export BibTeX, insert citation keys into LaTeX or Markdown drafts, read indexed full text when requested, and import BibTeX/RIS records into Zotero through the connector server. Use when the user mentions Zotero, citations, references.bib, BibTeX export, local Zotero API, localhost:23119, or adding citations from a Zotero library."
- use when: Find or cite a paper from my Zotero library, export `references.bib`, insert citation keys into a LaTeX or Markdown draft, or import BibTeX/RIS into Zotero.
- needs: Zotero Desktop with its local API on port 23119, Python 3; no API key for reads.
- side effects: may edit Zotero `prefs.js` (timestamped backup) and restart Zotero; writes `.bib`, draft and requested full-text files; imports change the selected library/collection. SKILL.md waives the source/destination confirmation when import was explicitly requested; the route reference does not. Take the stricter reading: tell the user to expect a confirmation of record and target (the collection currently selected in Zotero) before every import.
