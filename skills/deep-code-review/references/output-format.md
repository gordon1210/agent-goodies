# Output Format

## Default report

Lead with findings ordered by severity, then location. Do not pad the report with generic praise, a checklist transcript, or style commentary.

For each finding use:

```markdown
### [HIGH] Preserve the tenant predicate when loading invoices

`src/billing/invoices.ts:84-91`

The changed lookup now filters only by invoice ID. An authenticated user who knows an invoice ID from another tenant reaches this handler and receives that invoice because the route middleware authenticates the user but does not add object-level authorization.

- **Trigger:** User from tenant A requests an invoice ID owned by tenant B.
- **Impact:** Cross-tenant disclosure of invoice and customer data.
- **Evidence:** Trace `GET /invoices/:id` → `getInvoice()` → changed query; no later ownership check; the base query included `tenant_id`.
- **Fix direction:** Include the trusted tenant ID in the database predicate or enforce equivalent object authorization before returning the record.
- **Confidence:** Strong
```

The prose may be shorter when trigger, impact, and evidence fit clearly in one paragraph. Keep the title specific to the broken invariant, not the generic category.

## Location

- Anchor to the smallest changed line that causes the defect.
- When the cause is an omission, anchor to the changed block where the missing operation belongs.
- Mention relevant unchanged callers or guards in Evidence, but do not pretend they were changed.
- Use repository-relative paths and exact line ranges when available.

## Finding quality

Every finding must let a maintainer answer:

1. What exactly is wrong?
2. Under what concrete condition does it happen?
3. Why does existing code not prevent it?
4. What is the user, security, data, deployment, or operational impact?
5. Why was this introduced by the reviewed change?
6. What is the narrow fix direction?

Do not include a finding if one of the first five answers is missing.

## Concision

- One root cause, one finding.
- Do not list every affected caller when one representative path plus blast-radius statement is sufficient.
- Do not provide a full patch unless requested.
- Do not lecture about general best practices.
- Avoid hedging words when evidence is strong. Use explicit assumptions when it is conditional.

## Review summary

After findings, include only useful metadata:

```markdown
## Review summary

- **Verdict:** Block / Needs fixes / No blocking findings
- **Scope:** `<base>..<head>` or the exact reviewed files
- **Validation:** Commands run and their result
- **Not verified:** Relevant runtime, environment, generated output, or external-contract limitations
```

Verdict meanings:

- **Block:** at least one Confirmed/Strong Critical or High finding
- **Needs fixes:** no Critical/High, but one or more real Medium findings
- **No blocking findings:** no Confirmed/Strong Critical or High finding; this is not a proof of correctness

If there are no findings, say so directly and include scope and validation limits. Do not invent minor comments to make the review look productive.

## Conditional and pre-existing items

Keep them separate from findings:

```markdown
## Needs verification

- `[potential impact]` Candidate and the single unresolved premise needed to confirm it.
```

```markdown
## Pre-existing issues

- Issue, evidence that it predates the reviewed range, and whether the change materially worsens it.
```

Omit both sections when empty or not requested.

## Inline review comments

When the platform expects inline comments:

- Put severity in the title or first sentence.
- State trigger and impact in the first two sentences.
- Include only the decisive trace and fix direction.
- Keep extended investigation in the overall review summary if necessary.
- Never submit duplicate inline comments for the same root cause.
