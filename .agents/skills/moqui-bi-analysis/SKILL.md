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
5. When requested, create a LibreChat HTML artifact that renders a Chart.js chart from only those rows. Include the same bounded values in a visible HTML table below the chart.

## Chart.js artifacts

Create a named HTML artifact, not a Vega-Lite MIME artifact. For a bar chart, use a `<canvas>` and the pinned Chart.js 4.4.7 UMD bundle:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
```

- Put the returned data into a JavaScript literal using JSON serialization; never interpolate SQL text or unescaped values into HTML.
- Use no user-provided URL, script, iframe, network request, plugin, or external dataset other than the pinned Chart.js bundle.
- Use `responsive: true`, `maintainAspectRatio: false`, a visible title, labelled axes, and tooltips.
- Provide a table under the chart so the result remains available if Chart.js cannot load.
- Use only the bounded rows returned by `run_sql`; never synthesize or fetch more data.

## Vega-Lite export

LibreChat does not natively render `application/vnd.vegalite+json`. When the user explicitly requests Vega-Lite, provide the following v5 specification as a downloadable code block after the rendered Chart.js HTML artifact. Use only the returned rows in `data.values`:

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

Do not emit a Vega-Lite MIME artifact. The visual chart must be a native LibreChat HTML artifact using Chart.js; the Vega-Lite JSON is an optional portable export.

## Uploaded files and sandbox work

Use the isolated code sandbox only to inspect user-provided files, normalize data, calculate derived values, or generate reviewable artifacts. Keep input and generated files in the sandbox workspace. Do not write sandbox data to Moqui unless the user explicitly reviews the final result and requests a separate authorized Moqui action.

For a file analysis, show the detected schema, a small bounded preview, the transformation performed, and the chart specification or generated artifact. Do not claim a file was imported into Moqui unless an authorized Moqui tool completed that action.

## Response format

For a successful SQL analysis provide: the exact SQL used, a Markdown table, the number of returned rows, and (when requested) a rendered Chart.js HTML artifact plus an optional Vega-Lite export. For a blocked request provide: the exact tool error, the prerequisite or permission needed, and no fabricated output.
