-- From one partition of a norm (:agreement, :item) to the partitions of the other norms associated with it, both
-- directions, with kind, weight (confidence) and evidence. Read only. Example: EU-REG-2023-1230-EN / ANXIII.B.1.2.1
SELECT CASE WHEN f.AGREEMENT_ID = ':agreement' AND f.AGREEMENT_ITEM_SEQ_ID = ':item' THEN 'out' ELSE 'in' END AS dir,
       e.EDGE_TYPE_ENUM_ID AS kind, e.WEIGHT AS weight,
       CASE WHEN f.AGREEMENT_ID = ':agreement' AND f.AGREEMENT_ITEM_SEQ_ID = ':item' THEN t.LABEL ELSE f.LABEL END AS other,
       LEFT(CAST(p.TEXT_VALUE AS VARCHAR(4000)), 160) AS evidence
  FROM GRAPH_EDGE e
  JOIN GRAPH_VERTEX f ON f.GRAPH_VERTEX_ID = e.FROM_VERTEX_ID
  JOIN GRAPH_VERTEX t ON t.GRAPH_VERTEX_ID = e.TO_VERTEX_ID
  LEFT JOIN PARAMETER p ON p.GRAPH_ID = e.GRAPH_ID AND p.GRAPH_EDGE_ID = e.GRAPH_EDGE_ID AND p.PARAMETER_DEF_ID = 'CmpAssocEvidence'
 WHERE e.GRAPH_ID = 'NG_CMP_ASSOC'
   AND ((f.AGREEMENT_ID = ':agreement' AND f.AGREEMENT_ITEM_SEQ_ID = ':item') OR (t.AGREEMENT_ID = ':agreement' AND t.AGREEMENT_ITEM_SEQ_ID = ':item'))
 ORDER BY CASE WHEN e.EDGE_TYPE_ENUM_ID = 'CmpGaCites' THEN 1 ELSE 0 END, e.WEIGHT DESC
