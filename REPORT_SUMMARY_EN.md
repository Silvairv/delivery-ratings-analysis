# Report summary (English)

*Summary of [`Relatorio_Trabalho_Final.pdf`](Relatorio_Trabalho_Final.pdf), written in Portuguese. Author: Gabriel, November 2026.*

## Problem

In delivery operations, customer ratings are the main feedback on service quality, but only about 1 in 10 orders is rated. Understanding what makes a store get rated, and rated well, helps prioritize operational improvements.

**Business question:** how do order volume and kitchen prep performance (lateness and prep time) influence the ratings stores receive from customers?

**Data:** orders from 40 stores of a multi-brand dark kitchen operation (Sep–Oct 2026, anonymized): 40,177 orders and 48 variables from two management-panel exports. The analysis answers three questions:

1. How many orders per day does a store need before it has a realistic chance of being rated?
2. Does order volume change the quality of the ratings?
3. Do lateness and prep time reduce the share of 5-star ratings?

## Method

| Step | Decision | Why |
|---|---|---|
| Consolidation | Stacked the two monthly exports (`pd.concat`); 0 duplicate order IDs; 40 store names for 40 store IDs | Integrity checks before any analysis |
| Cancelled orders | Removed 3,658, leaving 36,519 valid orders | A cancelled order is not a sale and none had a rating |
| Missing ratings | Kept as `NaN` (3,510 rated orders, 9.6% of valid) | Null means the customer did not rate; filling it would create a rating nobody gave |
| Rating scale | Divided by 100 (scale 100–500 to 1–5) | Comparable, readable scale |
| Prep time | Text with decimal comma converted to numeric | Required for averages and buckets |
| Prep time = 0 | 4,156 orders (11.4%) treated as "not measured" and set to `NaN` | All have "ready for pickup" = No; the zero means the store never marked the order ready, not an instant prep. Keeping zeros would drop mean prep from 16.8 to 14.9 min and inflate the 0–10 min bucket (8,132 to 12,288 orders) |
| Feature engineering | Prep-time buckets (0–10, 11–20, 21–30, 31–40, 41+ min), orders-per-day buckets (1–5, 6–10, 11–15, 16–20, 21+), 2,175 store-day records, 5-star flag, month, brand | Enables the comparisons above |

**Who rates?** Rated and unrated orders differ little in mean prep time (17.6 vs 16.7 min) and lateness (25.2% vs 23.7%), but this does not prove the absence of response bias.

## Results

- **Volume drives the chance of being rated.** The chance a store gets at least one rating in a day rises from 27% (1–5 orders) to 53%, 71%, 77% and 93% (21+ orders). Part of this is mechanical: with only 9.6% of orders rated, more orders mean more chances.
- **Volume does not drive rating quality.** The share of 5-star ratings is 68.7% in the 1–5 orders bucket (only 115 ratings) and stable at 77–78% from 6 orders/day.
- **Prep time is right-skewed.** Among 32,363 orders with measured prep time, the median is 15 min and 90.8% are ready within 30 min; the long tail reaches 161 min.
- **Prep time drives rating quality.** Average rating falls from 4.60 (up to 10 min) to 4.46 (11–30), 4.28 (31–40) and 3.90 (41+); the 5-star share falls from 83.5% to 56.7%. The drop is small up to 30 min and sharper after.
- **Lateness flips between 20 and 30 minutes.** Late-flagged orders: 3% up to 10 min, 11% at 11–20, 53% at 21–30, then 97–99%. Lateness rises before ratings clearly drop (after 30 min).

## Conclusion

Order volume influences *whether* a store is rated, not *how well*. Prep performance influences *how well*: from up to 10 min to 41+ min, the average rating falls from 4.60 to 3.90 and the 5-star share from 83.5% to 56.7%.

**For operations:** keeping prep time within 20–30 minutes protects the rating; getting more orders rated requires volume, not faster prep.

## Limitations

- Results are associations, not proof of causation.
- Only 9.6% of orders are rated, and raters may not represent all customers.
- The 41+ min bucket has only 134 ratings, so it is less stable.
- Store, brand and time-of-day effects are not separated. **Next step:** compare brands and cities.
