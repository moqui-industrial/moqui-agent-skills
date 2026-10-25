-- Hook -> the requirements its items cite (second step of hook-items.sql). Read only.
-- Parameter :hook = concept key (iac-sl-2: security level IAC 2 of IEC 62443). The items linked to the concept
-- (SL lists, Annex B rows) cite requirements by identifier ("CR 1.1 (1)"); the references reach their items.
SELECT DISTINCT a.TO_AGREEMENT_ID norm, a.ASSOC_TEXT cited, t.AGREEMENT_ITEM_SEQ_ID item,
       COALESCE(t.ITEM_TITLE, LEFT(t.ITEM_TEXT, 90)) title
  FROM PARAMETER k
  JOIN PARAMETER ci ON ci.GRAPH_VERTEX_ID = k.GRAPH_VERTEX_ID AND ci.PARAMETER_DEF_ID = 'CmpConceptItem'
  JOIN AGREEMENT_ASSOC a ON a.AGREEMENT_ID = ci.AGREEMENT_ID AND a.AGREEMENT_ITEM_SEQ_ID = ci.AGREEMENT_ITEM_SEQ_ID
       AND a.AGREEMENT_ASSOC_TYPE_ENUM_ID = 'AatReference' AND a.TO_AGREEMENT_ITEM_SEQ_ID IS NOT NULL
  JOIN AGREEMENT_ITEM t ON t.AGREEMENT_ID = a.TO_AGREEMENT_ID AND t.AGREEMENT_ITEM_SEQ_ID = a.TO_AGREEMENT_ITEM_SEQ_ID
 WHERE k.GRAPH_ID = 'NG_CMP_VOCABULARY' AND k.PARAMETER_DEF_ID = 'CmpConceptKey' AND k.SYMBOLIC_VALUE = ':hook'
 ORDER BY a.TO_AGREEMENT_ID, t.AGREEMENT_ITEM_SEQ_ID
