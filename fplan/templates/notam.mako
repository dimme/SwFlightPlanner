<%inherit file="base.mako"/>

<script src="/notam.js" type="text/javascript">
</script>
<script src="/MochiKit.js" type="text/javascript">
</script>
<script type="text/javascript">
marknotamurl='${h.url_for(controller="notam",action="mark")}';
function navigate_to(where)
{	
	window.location.href=where;
}

</script>

<div id="notamcontent" style="height:100%;width:100%;overflow:auto;">

<table>
<tr>
<td>Read</td><td> 
<form action="${h.url_for(controller="notam",action="markall")}" method="POST">
Notam <input type="submit" style="font-size:10px" value="Mark all read"/>
</form>
</td>
</tr>
%for notamupdate in c.notamupdates:
<tr id="notamcolor_${notamupdate.appearnotam}_${notamupdate.appearline}" style="background:${'#b0ffb0' if (notamupdate.appearnotam,notamupdate.appearline) in c.acks else '#ffd0b0'}">
<td>
<input onchange="click_item(${notamupdate.appearnotam},${notamupdate.appearline},1);return true" type="checkbox" id="notam_${notamupdate.appearnotam}_${notamupdate.appearline}" 
${'checked="1"' if (notamupdate.appearnotam,notamupdate.appearline) in c.acks else ''|n}/>
</td>
<td>
<div style="font-size:10px">
<b>${notamupdate.category}</b> 
</div>
<div style="font-size:12px;cursor:pointer" onclick="click_item(${notamupdate.appearnotam},${notamupdate.appearline},0);return true" >
%for line in notamupdate.text.splitlines():
${line}<br/>
%endfor
</div>
<div style="font-size:10px">
Downloaded: <b>${notamupdate.notam.downloaded.strftime("%Y%m%d %H%M")}</b> <b><u>
<a href="${h.url_for(controller="notam",action="show_ctx",notam=notamupdate.appearnotam,line=notamupdate.appearline)}#notam">
See original-&gt;
</a></u></b>
</div>
</div>
</td>
</tr>
%endfor
</table>
</div>


