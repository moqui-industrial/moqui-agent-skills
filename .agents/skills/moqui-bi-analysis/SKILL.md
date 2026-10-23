---
name: moqui-bi-analysis
description: Analyze authorized Moqui DataDocuments with the moqui MCP run_sql tool, return bounded Markdown results, and create safe Vega-Lite specifications from returned rows. Use for BI exploration, SQL analysis, DataDocument reporting, and chart specifications without bypassing Moqui authorization.
---

# Moqui BI analysis

Use this skill for exploratory analysis of a Moqui DataDocument through LibreChat and the `moqui` MCP server. The current Moqui user and the artifact-aware security rules remain the authorization boundary.

## Tool contract

Call `run_sql` only through the `moqui` MCP server. It accepts a single read-only `SELECT` or `WITH` query and verifies the referenced physical DataDocument indexes against the current user's permissions before submitting it to OpenSearch SQL.

- Use lower-snake-case DataDocument index names, for example `mantle_product`.
- End every query with a literal `LIMIT`; use `LIMIT 20` for an exploratory request unless the user asks for a smaller result.
- Pass `maxRows` equal to the SQL limit, never greater than `500`.
- Never query Moqui entity tables, internal indexes, system tables, or an index not explicitly named by the user.
- Do not use DDL, DML, joins to unapproved indexes, comments, multiple statements, or vendor-specific write operations.
- If the tool reports an authorization or SQL-plugin error, report it plainly. Do not invent rows, aggregates, or charts.

## Analysis workflow

1. Restate the requested DataDocument and metric briefly.
2. Build one bounded query with explicit columns. For a product-type chart, aggregate the type and count in the same query:

   ```sql
   SELECT productTypeEnumId, COUNT(*) AS productCount
   FROM mantle_product
   GROUP BY productTypeId
   ORDER BY productCount DESC
   LIMIT 20
   ```

3. Call `run_sql` with the query and matching `maxRows`.
4. Render the returned rows as a Markdown table. Preserve returned column names and show only the returned rows.
5. When requested, return a Vega-Lite v5 specification with inline `data.values` copied only from those rows. Use no external URL, JavaScript expression, transform that fetches data, or hidden source.

## Vega-Lite template

Use a simple accessible bar chart when the result has a category and a numeric measure:

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "Products by product type",
  "data": {"values": []},
  "mark": "bar",
  "encoding": {
    "x": {"field": "productCount", "type": "quantitative", "title": "Products"},
    "y": {"field": "productTypeEnumId", "type": "nominal", "sort": "-x", "title": "Product type"},
    "tooltip": [
      {"field": "productTypeEnumId", "type": "nominal"},
      {"field": "productCount", "type": "quantitative"}
    ]
  }
}
```

Mark a chart artifact as `application/vnd.vegalite+json` when the client supports that MIME type. If it renders as JSON, still provide the valid specification and state that the LibreChat Vega-Lite renderer is not installed or enabled.

## Uploaded files and sandbox work

Use the isolated code sandbox only to inspect user-provided files, normalize data, calculate derived values, or generate reviewable artifacts. Keep input and generated files in the sandbox workspace. Do not write sandbox data to Moqui unless the user explicitly reviews the final result and requests a separate authorized Moqui action.

For a file analysis, show the detected schema, a small bounded preview, the transformation performed, and the chart specification or generated artifact. Do not claim a file was imported into Moqui unless an authorized Moqui tool completed that action.

## Response format

For a successful SQL analysis provide: the exact SQL used, a Markdown table, the number of returned rows, and (when requested) the Vega-Lite specification/artifact. For a blocked request provide: the exact tool error, the prerequisite or permission needed, and no fabricated output.
