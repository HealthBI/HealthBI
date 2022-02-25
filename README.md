# HealthBI

HealthBI.py is the main script.
<br>
Usage: `python HealthBI.py filename`

healthBI --> takes and parses both csv and json. 
--> creating a list of unique temporal, location, and indicators objects. 
- row 0:
    + temporal.appendIfNew(temporal0)
    + 
Fact0(temporal0.uid :uid + location0.uid :none + indicator0.uid + real value0)
- row 1:
Fact1(temporal0 + location0 + indicator1 + real value1)
- row 2:
Fact2(temporal1 + location1 + indicator1 + real value2)
...
- row 200:
...

-- Facts = (fact1, fact2)
-- temporals = [temporal0, temporal1]
   + uid = insertToDB(temporal0) 
   + temporal0.uid = uid
-- locations = [location0, location1]
