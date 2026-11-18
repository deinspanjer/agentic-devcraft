# anthropics/skills far from development: office documents and business writing
Source: https://github.com/anthropics/skills @ e4bb5d960d87126ff3b3a8af1a104b7db67560ba
Distribution (anthropics/skills): the Claude Code plugin marketplace `anthropic-agent-skills` (`/plugin marketplace add anthropics/skills`, then `/plugin install <plugin>@anthropic-agent-skills`). Skill directories are `skills/<skill>/`.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in anthropic.md. Families here: `document-skills`, `example-skills (internal-comms)`.

## Family: document-skills (anthropics/skills)
- source repo: https://github.com/anthropics/skills (entry `document-skills`: skills/xlsx, docx, pptx, pdf)
- manifest notes: Claude marketplace manifest only; no Codex or Cursor manifest. No MCP servers, app connectors, hooks, commands or agents; no auth policy. Skills ship their own scripts. They were written for Anthropic surfaces ("preinstalled" tools, a sandbox `soffice` wrapper), so in another host each tool is a requirement to check.
- router: none. The trigger is the file extension; no skill invokes another.
- development distance: far (office documents)
- disclosure recommendation: simple. Four independent file-format skills chosen by extension; short records are enough.

### docx
- id: document-skills:docx (source path: skills/docx/SKILL.md)
- description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
- use when: "Make, edit or read this Word file": reports, memos, letters, templates, tracked changes, comments, tables of contents, find-and-replace in a .docx or .dotx.
- not for: `pdf` (PDF files), `xlsx` (spreadsheets), `pptx` (slides), `doc-coauthoring` (deciding what the document says; docx is file mechanics only). Google Docs is excluded.
- needs: Node with npm `docx`, `pandoc`, LibreOffice, `pdftoppm`, Python `defusedxml`.
- side effects: writes local files. A comment stays invisible until its anchor markers are inserted in `word/document.xml`; accepting changes can leave empty paragraphs, so check the XML.
- part of: standalone; can follow `doc-coauthoring`.

### pdf
- id: document-skills:pdf (source path: skills/pdf/SKILL.md)
- description: "Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill."
- use when: "Do something with this PDF": extract text or tables, merge, split, rotate, watermark, create, fill a form, encrypt or decrypt (known password), extract images, OCR a scan.
- not for: art direction (`canvas-design`) or native Word/slide/spreadsheet editing (`docx`, `pptx`, `xlsx`); PDF output still falls within its broad trigger.
- needs: task-dependent Python libraries `pypdf`, `pdfplumber`, `reportlab`, `pandas`; Poppler, `qpdf`; Tesseract, `pytesseract` and `pdf2image` for OCR; image viewing for form filling (`FORMS.md`).
- side effects: writes local files. Forms without fillable fields get text annotations over the page, not real fields.
- part of: standalone; forms hand off to `FORMS.md` inside the skill.

### pptx
- id: document-skills:pptx (source path: skills/pptx/SKILL.md)
- description: "Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user mentions "deck," "slides," "presentation," or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. If a .pptx or .potx file needs to be opened, created, or touched, use this skill."
- use when: "Build, edit, read or split this deck": pitch decks, slides, speaker notes, templates, .pptx or .potx, even only to extract text.
- not for: standalone art (`canvas-design`), Word files (`docx`) or PDF processing (`pdf`); `theme-factory` can supply a preset look alongside pptx's own theme mechanism.
- needs: Node `pptxgenjs`; Python `python-pptx`, Pillow, `defusedxml`, `lxml`; LibreOffice via `scripts/office/soffice.py`; `pdftoppm`; image viewing for the required visual QA.
- side effects: writes local files. `add_slide.py` without `-o` rewrites the input deck, and a duplicated slide shares chart and embedded-object parts with the original.
- part of: standalone, with a required three-step QA (content, file, visual).

### xlsx
- id: document-skills:xlsx (source path: skills/xlsx/SKILL.md)
- description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like "the xlsx in my downloads") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
- use when: "Fix, build or clean this spreadsheet": formulas, formatting, charts, messy .csv or .tsv into a proper workbook; the deliverable is a spreadsheet file.
- not for: `docx` (Word report), `pdf` (extract tables from a PDF first), standalone Python scripts, database pipelines, Google Sheets API work.
- needs: Python `openpyxl`, `pandas`, `markitdown`; LibreOffice for `scripts/recalc.py`.
- side effects: writes local files. Saving with `data_only=True` destroys formulas; `.xlsm` macros require `keep_vba=True`, and openpyxl saves can drop text boxes, shapes and slicers. `recalc.py` is mandatory with formulas; preserve `not_computed` formulas and sound dependents, and disclose missing/stale caches or fallback values.
- part of: standalone.

## Family: example-skills (anthropics/skills; far members: internal-comms)
- source repo: https://github.com/anthropics/skills (entry `example-skills`). The family header and its core-dev and adjacent records are in ../families/example-skills.md.
- manifest notes: Claude marketplace manifest only; no MCP servers, app connectors, hooks, commands or agents; no auth policy. Written for Anthropic surfaces.
- router: none.
- development distance: far

### internal-comms
- id: example-skills:internal-comms (source path: skills/internal-comms/SKILL.md)
- description: "A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.)."
- use when: write a 3P update, newsletter, FAQ answer, status or incident report from four generic example formats.
- not for: `doc-coauthoring` (long structured specs).
- needs: bundled `examples/` guidelines; connected Slack, Drive, email or calendar for gathering company context when available, otherwise user-supplied material.
- side effects: none; drafts only, sends nothing.
- part of: entry router among its own four example files.
