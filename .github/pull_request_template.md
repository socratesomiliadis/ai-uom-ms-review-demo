## Classroom demonstration: extract pricing constants without changing behavior

This PR extracts named constants for the eligibility threshold, discount rate, and discount cap. It deliberately includes a regression for a software engineering lecture. It is a handwritten teaching fixture, not a recorded model output. Do not merge a failing version. The repair must preserve the constants refactor while restoring the contract.

### Intended behavior

Keep the public `PriceCalculator.calculate(BigDecimal subtotal, String coupon)` API and all requirements in `ticket.md`.

- STUDENT10 applies when subtotal is at least 50.00.
- Discount is 10%, capped at 20.00.
- Round the discount to two decimal places with HALF_UP before subtracting it.
- Preserve validation, coupon normalization, and output scale 2.

### Evidence

GitHub acceptance run: NOT RUN / replace with the actual run URL.
Tested checkout SHA and PR head SHA: NOT VERIFIED / copy from the actual report.
CodeRabbit review: NOT RUN / link the actual finding after review.

Inspect the actual diff and reports. Keep acceptance tests and CI configuration unchanged. Update this description after the final fix and evaluation.
