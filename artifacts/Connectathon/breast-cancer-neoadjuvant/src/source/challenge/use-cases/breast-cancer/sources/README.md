# Breast cancer source corpus

This corpus supplies unstructured online material for the breast cancer workshop, following the STEADI source-manifest pattern. It combines two linked ASCO guideline publications with four locally usable NCI text extractions. The sources serve different purposes; they are not interchangeable votes for one treatment rule.

The retrieval date is **September 19, 2026**. Each included source records the date actually displayed on the page as well as the retrieval timestamp. A recent retrieval does not mean a recent evidence review or establish that this is an exhaustive collection of current guidance.

## Reading and mining order

1. Read [ASCO 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8274745/), recommendations **3.1 and 3.2**, for the historical TNBC neoadjuvant decision boundary used in this exercise. Keep the distinction between clinically node-positive disease and cT1a/b N0 disease. Do not turn a missing receptor or staging value into a negative result.
2. Read the [ASCO 2022 rapid recommendation update](https://ascopubs.org/doi/abs/10.1200/JCO.22.00503) ([PubMed metadata](https://pubmed.ncbi.nlm.nih.gov/35417251/)) before discussing immunotherapy. It updates the 2021 evidence context. A broad flag to review neoadjuvant therapy does not establish pembrolizumab eligibility. Publisher search exposed the update's abstract; direct full-page retrieval failed during this task, so its full text is not supplied here.
3. Mine [NCI professional treatment excerpts](raw/nci-breast-treatment-pdq.txt) for subtype definition, preoperative treatment context, trial evidence, and adverse-event context. The selected source sections are `_3053` and `_2896`; citations retain links to the original page. This is an evidence synthesis, not a formal practice guideline. The retrieved page displayed **April 25, 2025** and contains evidence-time qualifiers such as immature EFS data; preserve those qualifiers rather than claiming this is the latest trial follow-up.
4. Use [NCI TNM staging text](raw/nci-breast-tnm.txt) to discuss T-category boundaries and the distinction between T, N, M, grade, and biomarkers. Its N section explicitly describes **pathological** staging and does **not** define clinical cN. Do not infer clinical cN from pathological node counts or derive an entire stage group from tumor diameter.
5. Use [NCI chemotherapy text](raw/nci-breast-chemotherapy.txt) and [NCI immunotherapy text](raw/nci-breast-immunotherapy.txt) for patient-facing explanations of treatment before and after surgery. These patient education pages are not authority for exact regimen eligibility, dosing, or treatment orders.

The [manifest](manifest.yaml) gives stable source IDs, online URLs, local paths, roles, locators, and provenance. When recording a mined assertion, carry the source ID, recommendation or section locator, source date, retrieval date, and whether the assertion is quoted source content or a workshop interpretation. Preserve disagreement and changed evidence; do not silently combine the 2021 and 2022 recommendations into a timeless rule.

## What is stored

The `raw/*.txt` files are **selected unstructured source prose**, not author-written clinical summaries, complete source-page snapshots, or computable rules. Original wording is preserved, with whitespace normalization, paragraph/list boundaries, resolved hyperlink destinations, and an added provenance header. The patient pages contain article introduction/body prose; the professional page contains only the selected TNBC sections.

All tables, figures, images, captions, image components, navigation, scripts, and unselected sections are excluded. In particular, the professional page's separately credited AJCC tables are not redistributed. The original HTML is fetched only in memory. Its byte count and SHA-256 are recorded independently of the saved text's byte count and SHA-256, so the manifest does not misrepresent an extraction as an untouched response.

Text is adapted from the National Cancer Institute under its [reuse policy](https://www.cancer.gov/policies/copyright-reuse), with attribution to and links to each original publication. The PDQ excerpts are **not** the complete, maintained NCI PDQ cancer information summary. See the original page's [permission section](https://www.cancer.gov/types/breast/hp/breast-treatment-pdq#_AboutThis_12). ASCO publications remain link-only because publicly readable content does not imply redistribution permission.

## Refresh and verify

Run from the repository root:

```sh
uv run use-cases/breast-cancer/sources/retrieve.py
```

The script declares pinned Beautiful Soup and PyYAML dependencies, downloads the four NCI pages over HTTPS, checks that every configured selector identifies exactly one element, writes the extracts, and refreshes their manifest entries. Existing link-only entries are preserved. It does not reverify the linked ASCO publications or update their verification dates. Review the resulting diff: source HTML, dates, selectors, treatment context, and permissions can change. The original response hash is an audit record, not a promise that a later HTTP request reproduces identical HTML.

Verify stored files independently:

```sh
uv run --with pyyaml python - <<'PY'
from hashlib import sha256
from pathlib import Path
import yaml
manifest = yaml.safe_load(Path('use-cases/breast-cancer/sources/manifest.yaml').read_text())
for source in manifest['included_sources']:
    data = Path(source['local_path']).read_bytes()
    assert len(data) == source['bytes'], source['id']
    assert sha256(data).hexdigest() == source['sha256'], source['id']
print('Verified all included source sizes and SHA-256 hashes')
PY
```

This corpus supports a nonmetastatic TNBC **oncology-review flag** demonstration. It does not prescribe therapy, establish treatment fitness, or replace oncology review. Missing and conflicting clinical facts remain explicit in the associated patient cases.
