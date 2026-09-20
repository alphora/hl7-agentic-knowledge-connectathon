#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["beautifulsoup4==4.14.3", "PyYAML==6.0.3"]
# ///
"""Retrieve selected NCI prose, excluding tables/images and preserving provenance.

Run from any directory: uv run path/to/sources/retrieve.py
Writes only this sources directory. Live revisions can change hashes and content;
review the diff before adopting refreshed material. HTML responses stay in memory.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, NavigableString
import yaml

HERE = Path(__file__).resolve().parent
PREFIX = "use-cases/breast-cancer/sources/"
POLICY = "https://www.cancer.gov/policies/copyright-reuse"
SOURCES = [
    {
        "id": "nci-breast-treatment-pdq",
        "title": "Breast Cancer Treatment (PDQ®)–Health Professional Version",
        "canonical_url": "https://www.cancer.gov/types/breast/hp/breast-treatment-pdq",
        "role": ["professional-evidence-summary", "receptor-status", "neoadjuvant-context"],
        "selectors": ["#_3053", "#_2896"],
        "locators": [
            {"section_id": "_1027", "heading": "Stages I, II, and III Triple-Negative Breast Cancer (TNBC)", "selection": "Opening definition paragraph _3053 only"},
            {"section_id": "_2896", "heading": "Preoperative therapy for TNBC", "selection": "Section prose including Chemotherapy and Immunotherapy subsections; tables/images excluded"},
        ],
        "boundary": "Professional evidence synthesis, not a formal clinical-practice recommendation. Static selected excerpts are not the complete maintained PDQ summary. Trial eligibility and results do not independently establish this demonstration's decision rule.",
    },
    {
        "id": "nci-breast-tnm",
        "title": "TNM Staging for Breast Cancer",
        "canonical_url": "https://www.cancer.gov/types/breast/stages/tnm-staging-system",
        "role": ["patient-education", "staging-context"],
        "selectors": ["article .cgdp-field-intro-text", "article .cgdp-article-body"],
        "locators": [{"heading": "Tumor (T)"}, {"heading": "Lymph node (N)"}, {"heading": "Metastasis (M)"}],
        "boundary": "Patient education. T size boundaries provide context; do not infer T category from size alone when invasion features matter. The N section explicitly describes pathological staging and must not be used to derive clinical cN from node counts.",
    },
    {
        "id": "nci-breast-chemotherapy",
        "title": "Chemotherapy for Breast Cancer",
        "canonical_url": "https://www.cancer.gov/types/breast/treatment/chemotherapy",
        "role": ["patient-education", "treatment-timing"],
        "selectors": ["article .cgdp-field-intro-text", "article .cgdp-article-body"],
        "locators": [{"section_id": "when-is-chemotherapy-for-breast-cancer-given", "heading": "When is chemotherapy for breast cancer given?"}],
        "boundary": "Patient education explains treatment timing and discussions; it is not sufficient authority for regimen selection or precise eligibility thresholds.",
    },
    {
        "id": "nci-breast-immunotherapy",
        "title": "Immunotherapy for Breast Cancer",
        "canonical_url": "https://www.cancer.gov/types/breast/treatment/immunotherapy",
        "role": ["patient-education", "updated-treatment-context"],
        "selectors": ["article .cgdp-field-intro-text", "article .cgdp-article-body"],
        "locators": [{"heading": "Who gets immunotherapy for breast cancer?"}, {"heading": "When is immunotherapy for breast cancer given?"}],
        "boundary": "Patient education supporting contemporary context; stage/subtype statements are not a substitute for the ASCO update and individualized oncology review.",
    },
]
EXCLUDED_TAGS = {"table", "figure", "figcaption", "img", "svg", "script", "style", "nav", "iframe", "video", "audio"}
BLOCK_TAGS = {"p", "div", "section", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6", "br"}

def prose(node, base):
    if isinstance(node, NavigableString):
        return str(node)
    if node.name in EXCLUDED_TAGS or "cgdp-image" in node.get("class", []):
        return ""
    body = "".join(prose(child, base) for child in node.children)
    if node.name == "a" and node.get("href") and body.strip():
        return f"{body.strip()} <{urljoin(base, node['href'])}>"
    if node.name in BLOCK_TAGS:
        return "\n" + ("- " if node.name == "li" else "") + body + "\n"
    return body


def main():
    manifest_path = HERE / "manifest.yaml"
    old = yaml.safe_load(manifest_path.read_text()) if manifest_path.exists() else {}
    included = []
    for source in SOURCES:
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        request = Request(source["canonical_url"], headers={"User-Agent": "Connectathon-source-corpus/1.0 (educational source provenance)"})
        with urlopen(request, timeout=45) as response:
            raw = response.read()
            original = {"retrieved_at": now, "resolved_url": response.url, "http_status": response.status,
                        "media_type": response.headers.get_content_type(), "bytes": len(raw), "sha256": sha256(raw).hexdigest(),
                        "stored": False, "reason_not_stored": "Original HTML includes images and potentially separately credited material; retain selected permitted prose only."}
        soup = BeautifulSoup(raw, "html.parser")
        page_dates = [x.get_text(" ", strip=True) for x in soup.select("article time")]
        pieces = []
        for selector in source["selectors"]:
            nodes = soup.select(selector)
            if len(nodes) != 1:
                raise RuntimeError(f"Expected one node for {source['id']} {selector}; got {len(nodes)}. Review source structure.")
            value = prose(nodes[0], source["canonical_url"])
            lines = [re.sub(r"\s+", " ", line).strip() for line in value.splitlines()]
            pieces.append("[Source selector: " + selector + "]\n" + "\n".join(x for x in lines if x))
        text = (f"Text extraction adapted from the National Cancer Institute\n"
                f"Original source title: {source['title']}\nOriginal source URL: {source['canonical_url']}\n"
                f"Retrieved at: {now}\nSource displayed date: {', '.join(page_dates)}\n"
                "Format: selected unstructured source prose; whitespace normalized and link destinations retained.\n"
                "Excluded: tables, images/figures/captions, page navigation, scripts, styling, and unselected sections.\n"
                "This is a static extraction, not the complete or maintained original publication.\n"
                f"Reuse policy: {POLICY}\n\n" + "\n\n".join(pieces) + "\n")
        saved = text.encode("utf-8")
        local = "raw/" + source["id"] + ".txt"
        (HERE / "raw").mkdir(exist_ok=True)
        (HERE / local).write_bytes(saved)
        included.append({key: value for key, value in source.items() if key not in {"selectors"}} | {
            "local_path": PREFIX + local, "media_type": "text/plain; charset=utf-8", "bytes": len(saved), "sha256": sha256(saved).hexdigest(),
            "source_displayed_dates": page_dates, "original_response": original,
            "extraction": {"script": PREFIX + "retrieve.py", "selectors": source["selectors"], "excluded_elements": sorted(EXCLUDED_TAGS) + [".cgdp-image"],
                           "transformations": ["Select source prose only", "Normalize whitespace and preserve paragraph/list boundaries", "Append resolved link destinations", "Prepend extraction and attribution metadata"]},
            "redistribution_basis": "NCI text reuse permission, except separately credited material. Selected prose excludes all tables, images and figures; attributed and labeled as an adaptation.",
            "license_url": POLICY,
        })
    manifest = {"version": "1.0.0", "status": "draft", "retrieved_at": datetime.now(timezone.utc).date().isoformat(),
                "checksum_algorithm": "sha256", "scope": "Educational TNBC neoadjuvant-review use case; not exhaustive current clinical guidance",
                "included_sources": included, "link_only_references": old.get("link_only_references", [])}
    manifest_path.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False, width=110))
    print(f"Retrieved {len(included)} selected text extracts; updated {manifest_path}")

if __name__ == "__main__":
    main()
