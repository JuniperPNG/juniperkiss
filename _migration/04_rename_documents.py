"""Rename the migrated Wix PDFs from their hashed filenames to readable slugs."""

from pathlib import Path

DOCS = Path(__file__).parent.parent / "assets" / "documents"

RENAMES = {
    "812149_1de328f4bd9541afa158ddca457d2cb3.pdf": "temperatures-role-in-fish-farming.pdf",
    "812149_5ef6c63f3dfd4772a8431609b2a0fb39.pdf": "tracking-an-illusion-of-technology.pdf",
    "812149_d308323a5aa54f95a8e8e75ff9b4aafa.pdf": "vegetation-survey-at-devils-dyke.pdf",
    "812149_3f99fedb7caf47bfbe392f7151714ad3.pdf": "comparing-invertebrate-sampling-techniques.pdf",
    "812149_40815d8788164e84bedb10368c8c7196.pdf": "winkle-stats.pdf",
    "812149_5429e31e4698454d99055cbb54aef2b2.pdf": "multivariate-analysis-of-resource-allocation.pdf",
    "812149_bd69b807b35242b788245348b2c48b9f.pdf": "long-term-ecological-research-lter.pdf",
    "812149_5a572a78f056479387bc5acafcac8d89.pdf": "northern-blotting-and-cdna-microarray-analysis.pdf",
    "812149_269bc6b4140e4e4f83846e1c2467e793.pdf": "green-revolution-genes-in-modern-crops.pdf",
    "812149_cb419b18a9dc406e88e905099e3ebb32.pdf": "can-subgenus-rubus-classification-rely-on-leaf-morphology.pdf",
    "812149_372c1c1113b14187a32e6a7f3abcd6bd.pdf": "critique-of-klingenberg-et-al-2012.pdf",
    "812149_9e3cfe40266047ff93c6e32b08a64e47.pdf": "agri-environment-farm-audit.pdf",
    "812149_2186d5caba3144cf8987096ec61d8f21.pdf": "identifying-conservation-units-of-mangroves.pdf",
    "812149_a8d6ad32ec44422690e7d1f2517819ac.pdf": "geometric-morphometrics-vs-traditional-methods.pdf",
    "812149_b5a0762114e140d58fdc38742b2db931.pdf": "pathogenicity-of-fusarium-oxysporum-fsp-cubense.pdf",
    "812149_1a52ed9719614048840a15e5a0b6fbde.pdf": "identification-of-pseudomonas-syringae-pathovars.pdf",
    "Document.pdf": "juniper-kiss-cv.pdf",
}

for old, new in RENAMES.items():
    src = DOCS / old
    if src.exists():
        src.replace(DOCS / new)
        print(f"{old} -> {new}")
    elif (DOCS / new).exists():
        print(f"already renamed: {new}")
    else:
        print(f"MISSING: {old}")
