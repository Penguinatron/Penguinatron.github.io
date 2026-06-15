import datetime

#converts a 'CSV' (with pipes (|) instead of commas(,)) into an HMTL document


print("defining pre-written sections")
notes = """This site is new- feel free to report any obvious errors via the contact links below"""

openingSection = """<!doctype html>
<html lang="en-GB">
<head>
<title>Hickies Workshop Status</title>

<link rel="stylesheet" href="style.css">
<base target="_parent">

</head>
<style>
	body{font-family: Helvetica, sans-serif;}
</style>
<body>
	
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

<p><a href="home.html">Back to main repair page</a></p>

<h1 style="text-align:center;">Oliver Hagen Workshop Status</h1>
"""

tableStart = """

	<table style="text-align:left; border-spacing:10px">
	  <tr>
		<th>Workshop Job Number</th>
		<th>Last Updated</th>
	    <th>Repair Brief</th>
		<th>Status</th>
	  </tr>
"""

closingSection = """

<h2>About:</h2>
<p>This quick, simple website shows all repairs currently in progress in the workshop, along with their status. This is updated at the end of each working day, so check back for progress.</p>
<p>If you don't see your Workshop Job Number in the list above, it's either not yet had work started, or has been completed and is awaiting collection. If you are unsure, feel free to get in touch via the details given below.</p>

<h2>Contact Us:</h2>
<p>Questions about the status of your instrument, or the repair services available? See below, and be sure to quote your Workshop Job Number for a quicker response.</p>

<h3>If your repair is via Hickies Music Shop:</h3>
<p>Give the shop a ring on <b>01189 575 771</b>, or <a href="mailto:admin@hickies.co.uk"><b>send an email</b></a>; someone will take a message and I'll get back to you ASAP. I usually work in the shop on all weekdays aside from Wednesdays.</p>
<h3>If your repair is via me directly:</h3>
<p><a href="mailto:ophagen@icloud.com"><b>Send me an email</b></a> and I'll get back to you as quickly as possible.</p>

<p></p>

<!--
tomato for delayed
cyan for parts on order
gold for progress
lime for nearly done
-->

</body>
</html>
"""

print("reading from CSV file")

file = open("currentRepairs.csv","r")
data = file.readlines()

print("extracting data")
workshopStatus = str("""<h2>"""+data[0].split("|")[0]+"""</h2>""")

tableLines = []

for currentLine in range(2,len(data)):
    RepairReference = str("<td>"+data[currentLine].split("|")[0]+"</td>")
    LastUpdated = str("<td>|"+data[currentLine].split("|")[1]+"|</td>")
    RepairBrief = str("<td>"+data[currentLine].split("|")[2]+"</td>")
    colour = "LightSkyBlue"
    Status = data[currentLine].split("|")[4].replace("\n","")
    if Status == "wip":
        colour = "gold"
    if Status == "delayed":
        colour = "tomato"
    if Status == "done":
        colour = "lime"
    #else:
    #    colour = "LightSkyBlue"
    Progress = str("""<td style="background-color:"""+colour+"""">"""+data[currentLine].split("|")[3]+"</td>")
    tableLines.append(str("<tr>"+RepairReference+LastUpdated+RepairBrief+Progress+"</tr>"))

n = len(tableLines)
for i in range(n-1):
  for j in range(n-i-1):
    if int(tableLines[j].split("|")[1].replace("-","")) < int(tableLines[j+1].split("|")[1].replace("-","")):
      tableLines[j+1], tableLines[j] = tableLines[j], tableLines[j+1]

file = open("workshopStatus.html","w")
print("writing to HTML document")
file.write(openingSection)
file.write(workshopStatus)
file.write(tableStart)
for count in range(0,len(tableLines)):
    file.write(str(tableLines[count].replace("|","")))
file.write("</table>")
file.write(str("<br><p>Last Updated "+str(datetime.datetime.now()))+"</p>")
file.write(str("""<p style="color:red"><b>"""+notes+"""</b></p>"""))
file.write(closingSection)

file.close()
print("done!")
