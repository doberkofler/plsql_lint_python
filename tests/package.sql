create or replace
package foo
is

procedure bar;

end;
/

create or replace
package body foo
is

procedure bar
is
begin
	null;
end;

end;
/
