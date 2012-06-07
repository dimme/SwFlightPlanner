
<%inherit file="base.mako"/>
<script src="/MochiKit.js" type="text/javascript"></script>

<script type="text/javascript">
function navigate_to(where)
{	
	function finish_nav()
	{				
		window.location.href=where;
	}
	finish_nav();
}

</script>
<div style="height:100%;width:100%;overflow:auto;">
<div>
<h1>Custom Data Sets</h1>

<b>WARNING! This function is under development and not for general use (yet)!</b>
%if c.flash:
<b>${c.flash}</b><br/>
%endif

<table>
<tr>
<td>Data Set</td><td>Active</td><td>Ready</td><td>Current(Latest)</td>
</tr>
%for item in c.items:
<tr>
<td><a href="${h.url_for(controller="customsets",setname=item['setname'],action="view",version=item['current'])}">${item['setname']}</a></td>
<td><a href="${h.url_for(controller="customsets",setname=item['setname'],action="view",version=item['active'])}">${item['active']}</a></td>
<td><a href="${h.url_for(controller="customsets",setname=item['setname'],action="view",version=item['ready'])}">${item['ready']}</a></td>
<td><a href="${h.url_for(controller="customsets",setname=item['setname'],action="view",version=item['current'])}">${item['current']}</a></td>
</tr>
%endfor
</table>


<a href="${h.url_for(controller="customsets",action="view",setname=c.newset,version="1")}">Create New</a>

</div>
</div>



