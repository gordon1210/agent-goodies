# Page route: commerce and purchase decisions

**Load when:** designing catalog, product detail, cart, or checkout-adjacent interfaces.

## The product and transaction outrank the effect

Make the item identifiable, comparable, and purchasable. Define product name,
variant, price/unit, availability, relevant delivery information, and the next action.
Do not apply a marketing hero pattern to every product detail page. Use the chosen
style for identity while keeping shopping conventions understandable.

## Catalog and product detail

Keep image framing consistent enough for comparison. Show real color and material;
artistic grayscale should not conceal a variant. Label unavailable options and
explain missing selections near the action. Provide usable search, sort, and filters
when the catalog warrants them. Preserve filter state in navigation when appropriate.

A gallery should have keyboard-operable controls and meaningful media descriptions.
Do not require hover to see essential product information. Provide size, scale,
materials, compatibility, or specifications in a readable structure rather than
burying them under decorative panels. Make price changes after variant selection clear.

A sticky purchase region can help long product pages only if it does not obscure
content, focus, or mobile keyboards. At high zoom and short viewport heights,
release sticky behavior before it traps the user in a partial panel.

## Transaction states

Distinguish adding, added, rejected, unavailable, and quantity-updated states. A
cart animation is not evidence the server accepted an operation. Preserve data
through recoverable errors and avoid duplicate submission. Keep totals and charges
consistent as the cart changes; do not fabricate a final total when required data
is unknown. Show transparent recovery when availability changes.

Use the project's approved payment and checkout flow. Do not add new payment
providers, collect sensitive fields, or implement transaction logic under a visual
design task. Keep cancellation and correction paths clear.

## Acceptance

Test missing variants, long names, unavailable products, loading images, failed cart
requests, currency formatting, error recovery, touch, and keyboard operation. Confirm
that product color information remains available without the artistic treatment.
A beautiful product image does not compensate for unclear price or purchase state.

Commerce details can have jurisdiction-specific requirements. Preserve supplied
policies and flag missing material rather than inventing legal compliance copy.
