-- Test: FactOrders.total_payment_value must exactly match SUM(FactPayments.payment_value).
-- Both are derived from the same raw payments table, so any divergence is a transformation bug.
-- Note: total_order_value (item prices) != total_payment_value intentionally — vouchers/discounts
-- mean customers sometimes pay less than the item total. That is expected Olist data behaviour.
-- Returns rows on failure.

WITH payment_totals AS (
    SELECT order_id, SUM(payment_value) AS sum_paid
    FROM `{{ env_var('GCP_PROJECT_ID', 'olist-analytics-01') }}.olist_analytics.FactPayments`
    GROUP BY order_id
)
SELECT
    fo.order_id,
    fo.total_payment_value,
    pt.sum_paid,
    ABS(fo.total_payment_value - pt.sum_paid) AS abs_diff
FROM `{{ env_var('GCP_PROJECT_ID', 'olist-analytics-01') }}.olist_analytics.FactOrders` fo
JOIN payment_totals pt USING (order_id)
WHERE ROUND(fo.total_payment_value, 2) != ROUND(pt.sum_paid, 2)
