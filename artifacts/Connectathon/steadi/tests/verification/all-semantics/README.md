# Synthetic all-branch semantics probe

CRL 6.4.2 / kit 2.13. Diagnostic only, not part of the clinical STEADI model or its emitted FHIR package.

Two selected Boolean publications are used in two shapes: independent `all:` sibling branches with an action per true branch, and nested A-then-B checks with an action only after both.

| Inputs | All siblings | Ordered checks |
|---|---|---|
| A true, B unknown | A Action produced; B reached and unknown | No action; pauses at B |
| A unknown, B true | B Action produced; A reached and unknown | No action; pauses at A |
| Both true | A Action and B Action produced | Not tested |
| Both unknown | No action; both reached and unknown | Not tested |

CRL and CEL validation pass without warnings. All six CRE assertions pass with no errors. Activity assertions check membership only; the complete produced sets and reached traces were also inspected for the table.

`all:` visits each sibling and can produce a known branch's action while another sibling is unknown. It is not an all-inputs-complete barrier. The missing input is still unknown; it does not erase the independently produced action.

This does not prove native $apply output, question collection, a viewer's global completion indicator, or how the three-question screen should be modeled. No native or emission tools were run. The synthetic package has two roots for separate CRE selection; it is not intended for FHIR emission. The empty src/cel/mv directory is required for classified regression validation and may need recreating after checkout.

Exact inputs are in src/crl/probe.crl and src/cel/regression/probe.cel. tool-calls.json records actual final MCP arguments; validation.json retains validation responses; run-decision.json is the exact returned CRE result text; summary.json records the produced sets.
