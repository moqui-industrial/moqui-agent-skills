<#-- Live zones and conduits of a system under consideration (IEC 62443-3-2 ZCR 3, ZCR 6.3-6.4): the function levels
     CmpDepSecurityZone / CmpDepSecConduit under the SUC product and their members. ?sucProductId=<productId>.
     html.ftl is FreeMarker only (no Markdown pass), the right type for a page that is mostly loops. -->
<#assign sucProductId = (ec.web.parameters.sucProductId)!"">
<#assign suc = ec.entity.find("mantle.product.Product").condition("productId", sucProductId).one()!>
<#assign fnAssocs = ec.entity.find("mantle.product.ProductAssoc").condition("productId", sucProductId)
        .condition("productAssocTypeEnumId", "CmpPatFunction").conditionDate("fromDate", "thruDate", ec.user.nowTimestamp).list()>
<#assign fnProducts = fnAssocs?map(a -> ec.entity.find("mantle.product.Product").condition("productId", a.toProductId).one())
        ?filter(p -> p.purposeEnumId! == "CmpDepSecurityZone" || p.purposeEnumId! == "CmpDepSecConduit")>
<h2>Zones and conduits of ${(suc.productName)!sucProductId}</h2>
<#if !suc?has_content>
<p class="text-danger">No product ${sucProductId}: pass ?sucProductId=&lt;root product of the SUC&gt;.</p>
<#elseif !fnProducts?has_content>
<p class="text-warning">No security zone or conduit is defined under this SUC (IEC 62443-3-2 ZCR 3.1: every asset belongs
to a zone or a conduit). Add them as function levels (add_function_product, purpose CmpDepSecurityZone /
CmpDepSecConduit).</p>
<#else>
<table class="table table-striped">
<thead><tr><th>Zone / conduit</th><th>Kind</th><th>Members (role)</th></tr></thead>
<tbody>
<#list fnProducts?sort_by("productName") as f>
<#assign members = ec.entity.find("mantle.product.ProductAssoc").condition("productId", f.productId)
        .condition("productAssocTypeEnumId", "CmpPatFunctionMember").conditionDate("fromDate", "thruDate", ec.user.nowTimestamp).list()>
<tr><td>${f.productName!f.productId}</td>
<td>${(f.purposeEnumId == "CmpDepSecurityZone")?then("zone", "conduit")}</td>
<td><#list members as m>${(ec.entity.find("mantle.product.Product").condition("productId", m.toProductId).one().productName)!m.toProductId}<#if m.purposeEnumId?has_content> (${m.purposeEnumId})</#if><#sep>, </#list></td></tr>
</#list>
</tbody>
</table>
</#if>
