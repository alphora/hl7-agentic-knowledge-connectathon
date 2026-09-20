# Explicit completed-negative result

The supplied fixture contract (`src/source/challenge/use-cases/breast-cancer/test-bundles/README.md`, Required expressions and Cases) distinguishes false applicability from unknown and states that false applicability does not mean treatment is unnecessary. The existing `eight-expression-contract` provenance cluster links that contract to the decision.

On 2026-09-20 the operator requested repair of the absent completed-negative terminal recommendation. `Nothing Recommended` is an explicit communication of the existing false applicability result, not an added clinical criterion or a recommendation against cancer treatment. Its payload limits the statement to this TNBC review rule. Source, anchors, clinical concepts and criteria are unchanged.

The two new otherwise branches communicate a false population gate or a false triple-negative/tumor-node gate. Ordered branch exclusions propagate unknown; the existing definitive-HER2 gate retains unresolved/equivocal handling. Five supplied false cases should produce this communication; four true cases retain Oncology Review Guidance; four unresolved cases produce neither. Native verification must inspect RequestGroup references and the actual CommunicationRequest, not just the absence of positive guidance.
