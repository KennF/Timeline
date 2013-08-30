from teamcity import app
from teamcity.config import DEBUG
from flask import url_for

print "server is running"
print app.__class__
app.run(debug=True)

