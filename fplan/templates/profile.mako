
<%inherit file="base.mako"/>

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

<div>
%if c.splash:
<span style="background:#ffb0b0">
${c.splash}
</span><br/>
%endif

<form method="POST" action="${h.url_for(controller="profile",action="save")}">
%if c.initial:
Choose a user name: <input type="text" name="username" value="" /><br/>
%endif
%if not c.initial:
Change name: <input type="text" name="username" value="${c.user}" /><br/> 
%endif

%if c.initial:
<div>
%endif
%if not c.initial:
<a href="#" onclick="document.getElementById('password').style.display='block'">Change password</a><br/>
<div id="password" style="display:none">
%endif
Enter a password: <input type="password" name="password1" value="" /><br/>
Enter password again: <input type="password" name="password2" value="" /><br/>
</div>
%if not c.initial:
Dotted track (faster, but less pretty): <input type="checkbox" name="fastmap" ${'checked="1"' if c.fastmap else ''|n}"/><br/>
%endif
<input type="submit" name="save" value="Save"/>
</form>

</div>

