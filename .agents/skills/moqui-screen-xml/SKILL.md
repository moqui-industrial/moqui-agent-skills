---
name: moqui-screen-xml
description: Create, review, or repair Moqui XML screens, transitions, forms, reports, and DbForm screens using the screen and form XSDs plus the established SimpleScreens conventions.
---

# Moqui XML screens

Create Moqui screens that are valid against the installed XSD and fit the conventions of the component that owns them. Use this skill for XML files below `screen/`, including transitions embedded in screens. Use `moqui-actions` as well whenever the screen contains an actions block or a transition with actions.

## Discover before writing

1. Locate the framework root and read `framework/xsd/xml-screen-3.xsd`; read `xml-form-3.xsd` for form fields and widgets. The XSD is the schema authority, not remembered element names or attributes.
2. Read the nearest parent screen, sibling screens, and the target component's `component.xml`. Preserve its navigation, permissions, rendering mode, and naming conventions.
3. For business entities, services, enums, or statuses, inspect their actual definitions before referring to them. Do not invent IDs, service names, field names, or status changes.
4. For a screen needing action logic, load the `moqui-actions` skill and use its validation/profile rules. Screens must not become a way to bypass service authorization or lifecycle services.

The principal local calibration source is `runtime/component/SimpleScreens`. Its 367 screen XML files are all well-formed, use `xml-screen-3.xsd`, and carry the same CC0 header. Read [SimpleScreens patterns](references/simplescreens-patterns.md) when selecting a screen shape or a special case.

## File skeleton and formatting

Start every new screen with the exact Moqui CC0 header and root form used in the local component:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
This software is in the public domain under CC0 1.0 Universal plus a
Grant of Patent License.

To the extent possible under law, the author(s) have dedicated all
copyright and related and neighboring rights to this software to the
public domain worldwide. This software is distributed without any
warranty.

You should have received a copy of the CC0 Public Domain Dedication
along with this software (see the LICENSE.md file). If not, see
<http://creativecommons.org/publicdomain/zero/1.0/>.
-->
<screen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/xml-screen-3.xsd">
    <!-- parameters, transitions, subscreens, actions, widgets -->
</screen>
```

- Keep XML declarations, namespace attributes, four-space indentation, element ordering, blank lines, and self-closing elements consistent with nearby screens.
- Add only screen attributes with a purpose: `default-menu-title`, `default-menu-index`, `default-menu-include`, menu image, authentication/authorization, or render behavior. Copy the closest peer rather than applying global defaults.
- Prefer one logical transition, action group, section, form, or field per line. Use compact one-line elements only where local source already does so.
- Use screen-relative locations for owned subscreens. Use `component://...` only for reusable artifacts or artifacts owned by another component.

## Build the screen in layers

Use the schema ordering. A typical business screen is:

1. required `<parameter>` declarations;
2. navigation and mutation `<transition>` declarations;
3. `<transition-include>` declarations for reusable selectors/endpoints;
4. `<subscreens>` when it owns children or cross-component children;
5. page-level `<actions>` for data shared by multiple widgets;
6. `<widgets>` with sections, forms, containers, labels, links, and panels.

Put data preparation nearest to its consumer: page-wide data belongs in screen `<actions>`; conditional or repeated data belongs in `<section>` or `<section-iterate>` actions; list queries belong inside their `form-list` when that makes the find/search contract explicit. Guard optional data with `condition`, `fail-widgets`, or clear errors instead of dereferencing null values.

## Navigation and transitions

- Declare every input to a transition with `<parameter>` when it is not implicit screen context. Mark genuinely required values `required="true"`.
- A navigation transition normally has only `<default-response url="..."/>`; use `//${appRoot}/...` only when routing across the application root is intended.
- A state-changing transition calls the owning business service and normally returns to the current screen with `<default-response url="."/>`.
- For data/download/AJAX endpoints, make the response semantics explicit: `read-only="true"` for reads and `<default-response type="none"/>` after a deliberate JSON, text, or resource response.
- Reuse selectors and endpoints with `<transition-include>` from the component `template/` directory. Do not copy a large shared transition into every screen.
- Preserve status transitions through the owning service. Do not directly update status-bearing entities from a screen.

## Forms, lists, and widgets

- Use `form-single` for a focused create, update, selector, or dialog operation; use `form-list` for editable or searchable lists. Set its `transition`, `list`, `multi`, and dialog/header options deliberately.
- Make required technical keys hidden fields. Give business fields concise localised titles through the normal form/widget mechanism; avoid exposing implementation keys as editable text.
- Use `auto-fields-entity` only after checking the entity and the desired field type. Explicit fields are preferable where label, widget, permissions, ordering, lookup behavior, or update semantics matter.
- Keep links and buttons tied to a declared transition. Use `link-type="hidden-form"` for a form-style state action, and add a confirmation for destructive or irreversible actions.
- Use `container-row`/`row-col`, `container-box`, `container-dialog`, `section`, and `section-iterate` as in adjacent screens. Give dialogs and reusable sections stable unique IDs/names.
- A complex detail screen may have several related panels, but each panel must have a clear ownership boundary and conditions derived from loaded data and permissions.

## Special screen types

- **Subscreen applications:** use `<subscreens>` plus `subscreens-panel` at the owner screen. Set menu metadata on owner/children rather than duplicating navigation links.
- **Reports:** use a service in actions to produce data, then `render-mode` for HTML/Quasar and export formats. Build download URLs from the screen URL instance and preserve required authorization checks before any dynamic report entity query.
- **DbForm:** manage `moqui.screen.form.DbForm` metadata through its services; render a runtime form with `form-single extends="DbForm#${formId}" dynamic="true"`. Keep `formLocation` and field/option mutations consistent with the standard Survey screens.
- **Print/email/resource endpoints:** use a dedicated render mode or response and the established template type (`xsl-fo`, CSV, Freemarker, etc.). Do not put binary/resource output into a normal page transition.

## Validate before handoff

1. Validate XML well-formedness: `xmllint --noout path/to/Screen.xml`.
2. Validate against the installed screen/form XSD using the repository's XML validation task or a JAXP/Xerces validator configured for Moqui's XSD imports.
3. Search the target component for every referenced transition, screen, service, entity, enum, and template; then validate action code with the `moqui-actions` workflow.
4. Open the parent path and the changed screen, exercising create/update/list/navigation and every affected render mode. Verify authorization failures are safe and expected.

Do not add an embedding/index for this skill: the XSDs and source patterns are local textual artifacts, and targeted search is more accurate and maintainable than a frozen vector index.
