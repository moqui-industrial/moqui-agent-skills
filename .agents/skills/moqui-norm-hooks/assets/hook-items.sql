-- Hook -> norm items (prepared query of the hook test suite, PLAN-NORMS-AGREEMENT.md WPE.1/E.3). Read only.
-- Parameter :hook = primary key of the hook record (ProductCategory, ProductFeature, ProductFeatureGroup, Enumeration).
-- The concept of the record, its broader concepts (transitively: a PLC is a control system) and its related concepts
-- (one step: safety logic unit) give the items that cite them; column via says which concept brought each item.
WITH RECURSIVE hook (vid) AS (
  SELECT GRAPH_VERTEX_ID FROM PARAMETER
   WHERE GRAPH_ID = 'NG_CMP_VOCABULARY' AND PARAMETER_DEF_ID = 'CmpConceptRecord' AND CAST(TEXT_VALUE AS VARCHAR(40)) = ':hook'
), up (vid, depth) AS (
  SELECT vid, 0 FROM hook
  UNION ALL
  SELECT e.TO_VERTEX_ID, up.depth + 1 FROM GRAPH_EDGE e JOIN up ON e.FROM_VERTEX_ID = up.vid
   WHERE e.GRAPH_ID = 'NG_CMP_VOCABULARY' AND e.EDGE_TYPE_ENUM_ID = 'CmpGetBroader' AND up.depth < 10
), concepts (vid, via) AS (
  SELECT vid, CASE WHEN depth = 0 THEN 'self' ELSE 'broader' END FROM up
  UNION
  SELECT CASE WHEN e.FROM_VERTEX_ID = h.vid THEN e.TO_VERTEX_ID ELSE e.FROM_VERTEX_ID END, 'related'
    FROM GRAPH_EDGE e JOIN hook h ON h.vid IN (e.FROM_VERTEX_ID, e.TO_VERTEX_ID)
   WHERE e.GRAPH_ID = 'NG_CMP_VOCABULARY' AND e.EDGE_TYPE_ENUM_ID = 'CmpGetRelated'
)
SELECT c.via, k.SYMBOLIC_VALUE concept, ci.TEXT_VALUE item, ci.PARAMETER_ENUM_ID role,
       par.ITEM_NUMBER parent_number, par.ITEM_TITLE parent_title, LEFT(ai.ITEM_TEXT, 120) text
  FROM concepts c
  JOIN PARAMETER k ON k.GRAPH_VERTEX_ID = c.vid AND k.PARAMETER_DEF_ID = 'CmpConceptKey'
  JOIN PARAMETER ci ON ci.GRAPH_VERTEX_ID = c.vid AND ci.PARAMETER_DEF_ID = 'CmpConceptItem'
  JOIN AGREEMENT_ITEM ai ON ai.AGREEMENT_ID = ci.SYMBOLIC_VALUE AND ai.AGREEMENT_ITEM_SEQ_ID = CAST(ci.TEXT_VALUE AS VARCHAR(40))
  LEFT JOIN AGREEMENT_ITEM par ON par.AGREEMENT_ID = ai.AGREEMENT_ID AND par.AGREEMENT_ITEM_SEQ_ID = ai.PARENT_ITEM_SEQ_ID
 WHERE k.SYMBOLIC_VALUE NOT IN ('machinery', 'related-product', 'reg-product', 'electrical-equipment')
 ORDER BY CASE c.via WHEN 'self' THEN 0 WHEN 'broader' THEN 1 ELSE 2 END, ai.AGREEMENT_ITEM_SEQ_ID
