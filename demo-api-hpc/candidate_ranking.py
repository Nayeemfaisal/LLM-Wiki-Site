"""Transparent ranking for source-audit planning.

This is deliberately not a model score. It only ranks what public-source
descriptions currently state, helping the team choose a small source audit.
"""


WEIGHTS = {
    "ts_eis_pairing": 3,
    "state_metadata": 2,
    "ageing_context": 1,
    "raw_access": 1,
    "license_clarity": 1,
    "schema_metadata": 1,
}


def priority_band(score):
    if score >= 8:
        return "audit first"
    if score >= 5:
        return "audit after first sample"
    return "reference or targeted audit"


def rank_candidates(candidates):
    """Return reproducible audit-planning ranks for candidate dictionaries."""
    ranked = []
    for candidate in candidates:
        evidence = candidate.get("evidence", {})
        contributions = {}
        for key, weight in WEIGHTS.items():
            evidence_level = evidence.get(key, 0)
            if not isinstance(evidence_level, int) or evidence_level < 0 or evidence_level > 2:
                raise ValueError(f"{candidate['id']} has invalid evidence level for {key}")
            contributions[key] = evidence_level * weight
        score = sum(contributions.values())
        ranked.append(
            {
                "id": candidate["id"],
                "name": candidate["name"],
                "role": candidate["role"],
                "score": score,
                "priority": priority_band(score),
                "score_breakdown": contributions,
                "audit_question": candidate["audit_question"],
                "source_url": candidate["source_url"],
            }
        )
    return sorted(ranked, key=lambda item: (-item["score"], item["name"]))
