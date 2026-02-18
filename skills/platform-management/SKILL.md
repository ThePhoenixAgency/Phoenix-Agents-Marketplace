---
name: platform-management
description: Bug Bounty platform management - submission, triage, communication
---

# Platform Management Skill

## When to Use

When managing the lifecycle of Bug Bounty reports across platforms.

## Pre-Submission Checklist

- [ ] Vulnerability is within program scope
- [ ] Program policy has been read entirely
- [ ] Steps are reproducible from scratch
- [ ] No PII/real user data in report
- [ ] Tokens/credentials are redacted in PoC
- [ ] CVSS score is justified
- [ ] Impact is quantified
- [ ] No duplicate (search resolved reports)

## Platform-Specific Notes

### HackerOne

- **Triage SLA**: Check program's response metrics
- **Severity**: Let the triager adjust, but justify your rating
- **Structured Scope**: Select the correct asset
- **Weakness type**: Map to correct CWE
- **Retesting**: Available after fix is deployed

### Bugcrowd

- **VRT**: Use Vulnerability Rating Taxonomy for classification
- **Priority**: P1 (Critical) to P5 (Informational)
- **Comments**: Platform logs all communication
- **Duplicate**: 48h window for same-day reports

### Intigriti

- **CVSS Calculator**: Built into submission form
- **Severity**: Auto-calculated from CVSS
- **Collaboration**: Can add collaborators to reports

### YesWeHack

- **French-friendly**: Reports in French accepted
- **CVSS**: Manual selection
- **Mediation**: Available for disputes

## Triage Response Templates

### Answering "Need More Info"

```
Hi [Triager],

Thank you for reviewing this report. Here is the additional information:

[Specific answer to their question]

I have also attached [screenshot/video/logs] demonstrating [specific aspect].

Please let me know if you need anything else.

Best regards
```

### Contesting a Severity Downgrade

```
Hi [Triager],

Thank you for your assessment. I would like to respectfully
challenge the severity rating for the following reasons:

1. [Factual argument with reference]
2. [Precedent: similar reports rated higher]
3. [Business impact quantification]

CVSS vector: [full vector string]

Similar reports:
- [Link to disclosed report 1]
- [Link to disclosed report 2]

I understand the final decision rests with the program team.

Best regards
```

### Contesting a Duplicate

```
Hi [Triager],

I understand this was marked as duplicate of report #[number].

However, I believe this is a distinct vulnerability because:
- [Technical difference 1]
- [Different root cause]
- [Different affected component]

Could you please review this again?

Best regards
```

## Payment Tracking

After resolution, pass to Bounty Finance:

```json
{
  "report_id": "H1-XXXXXX",
  "platform": "HackerOne",
  "program": "target-corp",
  "severity": "high",
  "submitted": "YYYY-MM-DD",
  "resolved": "YYYY-MM-DD",
  "amount": 0,
  "currency": "USD",
  "status": "resolved_pending_bounty"
}
```

## Metrics to Track

| Metric | Target |
|--------|--------|
| Response time (initial) | < 5 business days |
| Acceptance rate | > 50% |
| Average severity | Medium+ |
| Average payout | Program dependent |
| Invalid/NA rate | < 15% |
| Duplicate rate | < 10% |
