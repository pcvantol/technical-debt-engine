# Complexity metrics

Canonical metric namespace: `complexity.cyclomatic.average` and `.maximum` for all measured symbols, plus `complexity.cyclomatic.product.average` and `.product.maximum` for `PRODUCT_SOURCE` symbols. All are score-valued repository aggregates. `complexity.cyclomatic.distribution` is a count-valued four-band aggregate, also emitted for the product-repository scope. Future reserved concepts include median, p90, p95, cognitive complexity, nesting depth, essential complexity, and Halstead; none are implemented by this increment.
