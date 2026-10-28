<div>
<!-- Live status of a norm requirements project (mantle.compliance create#NormProject): ?projectId=<workEffortId>.
     Markdown runs before FreeMarker: FTL directives and comments only inside HTML blocks like this one. -->
<#assign projectId = (ec.web.parameters.projectId)!"">
<#assign project = ec.entity.find("mantle.work.effort.WorkEffort").condition("workEffortId", projectId).one()!>
<#assign efforts = ec.entity.find("mantle.work.effort.WorkEffort").condition("rootWorkEffortId", projectId).list()>
<#assign milestones = efforts?filter(w -> w.workEffortTypeEnumId! == "WetMilestone")>
<#assign tasks = efforts?filter(w -> w.workEffortTypeEnumId! == "WetTask")>
<#assign wrfs = ec.entity.find("mantle.request.requirement.WorkRequirementFulfillment")
        .condition("workEffortId", "in", tasks?map(w -> w.workEffortId)?sequence).list()>
<#assign reqs = ec.entity.find("mantle.request.requirement.Requirement")
        .condition("requirementId", "in", wrfs?map(f -> f.requirementId)?sequence).list()>
<#assign statuses = reqs?map(r -> r.statusId!"")?sequence?sort>
<h2>${(project.workEffortName)!projectId}</h2>
<p>Project <code>${projectId}</code>: ${reqs?size} norm requirements, ${tasks?size} tasks, ${milestones?size} milestones.</p>
</div>

## Requirements by status

A requirement is born *proposed*; a person approves or rejects it after review.

<table class="table table-striped">
<thead><tr><th>Status</th><th>Requirements</th></tr></thead>
<tbody>
<#list statuses as s><#if s?is_first || s != statuses[s?index - 1]>
<tr><td>${s}</td><td>${reqs?filter(r -> r.statusId! == s)?size}</td></tr>
</#if></#list>
</tbody>
</table>

## Milestones (one per norm)

<table class="table table-striped">
<thead><tr><th>Milestone</th><th>Tasks</th></tr></thead>
<tbody>
<#list milestones?sort_by("workEffortName") as m>
<tr><td>${m.workEffortName!m.workEffortId}</td><td>${tasks?filter(t -> t.parentWorkEffortId! == m.workEffortId)?size}</td></tr>
</#list>
</tbody>
</table>
