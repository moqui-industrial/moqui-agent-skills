---
name: moqui-bi-analysis
description: Analyze authorized Moqui DataDocuments with the moqui MCP run_sql tool, return bounded Markdown results, and create safe Chart.js artifacts from returned rows. Use for BI exploration, SQL analysis, DataDocument reporting, and charts without bypassing Moqui authorization.
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
5. When requested, emit a `chartjs` fenced JSON block from only those rows. LibreChat renders this bounded chart format inline in the conversation. Include the same bounded values in a Markdown table below the chart.

## Inline Chart.js format

Do not create HTML, SVG, React, a Canvas script, or a Vega-Lite MIME artifact. Emit exactly one JSON object in a `chartjs` fenced block using this format:

```chartjs
{
  "title": "Products by product type",
  "type": "bar",
  "labels": ["PtAsset", "PtDigitalAsset"],
  "datasets": [
    {"label": "Products", "data": [24, 1]}
  ]
}
```

- The accepted chart types are `bar`, `line`, `pie`, and `doughnut`; use `bar` for category counts.
- Use at most 100 labels and 8 datasets. Every dataset must have one finite number for each label.
- Copy values only from the bounded `run_sql` response. Do not include `options`, JavaScript, URLs, scripts, HTML, expressions, or unescaped content.
- The client supplies responsive layout, colours, labels, tooltips, and a pinned Chart.js runtime.
- Provide a Markdown table under the block so the result remains available if the client cannot load Chart.js.
- Use only the bounded rows returned by `run_sql`; never synthesize or fetch more data.

## Vega-Lite export

LibreChat does not natively render `application/vnd.vegalite+json`. When the user explicitly requests Vega-Lite, provide the following v5 specification as a downloadable code block after the rendered Chart.js block. Use only the returned rows in `data.values`:

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

Do not emit a Vega-Lite MIME artifact. The visual chart must use the inline `chartjs` block; the Vega-Lite JSON is an optional portable export.

## Uploaded files and sandbox work

Use the isolated code sandbox only to inspect user-provided files, normalize data, calculate derived values, or generate reviewable artifacts. Keep input and generated files in the sandbox workspace. Do not write sandbox data to Moqui unless the user explicitly reviews the final result and requests a separate authorized Moqui action.

For a file analysis, show the detected schema, a small bounded preview, the transformation performed, and the chart specification or generated artifact. Do not claim a file was imported into Moqui unless an authorized Moqui tool completed that action.

## Response format

For a successful SQL analysis provide: the exact SQL used, a Markdown table, the number of returned rows, and (when requested) an inline Chart.js block plus an optional Vega-Lite export. For a blocked request provide: the exact tool error, the prerequisite or permission needed, and no fabricated output.
