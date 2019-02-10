# Script to generate HTML (and javascript) file for searching through sentence
# completion norms.
#
# Run with:
#
#  $ python3 makehtml.py
#
# which will result in a self-contained sentences.html file that can be opened with
# a web browser.

path = 'sentences.html'

f = open(path, 'w')

longStr = """
<!DOCTYPE html>
<html lang="en-US">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Search 3085 sentence completion norms: Peelle et al.</title>

<style type="text/css">
body {
background:#ccc;
line-height: 1.2em;
}

#main {
width:80%;
margin:auto;
padding: 2em;
background: white;
}

#instructions {
border: 1px solid black;
padding: 1 em;
background:yellow;
}

</style>
"""

f.write(longStr)


# Javascript --------------------

longStr = """

<script type="text/javascript">

// Make array for sentences; we will loop through and add objects to
// hold sentence information
arrSentences = []

"""

f.write(longStr)


# Fill in array based on values --------------------

# Read in


# Loop over values and write in


longStr = """

"""

f.write(longStr)



# Functions to handle searching, etc. --------------------

longStr = """


</script>
"""


f.write(longStr)



# End head, add body

longStr = """
</head>
<body>
<div id="main">

<h1>Search 3085 sentence completion norms</h1>

<noscript>Javascript is required to run this code.</noscript>

<div id="instructions">

<p>This is an online search interface for completion norms for 3085 English sentences.</p>

<p>You can save this webpage to use on your local computer (using File > Save As from your menu) or by <a href="http://github.com/jpeelle/sentence-prediction/blog/example/html/sentences.html">downloading from GitHub</a>, which may run faster than the online version.</p>

<p>If you use these norms in scientific work, please cite:</p>

<p>Peelle JE, Rogers CS, Miller R, Spehar B, Sommers MS, Van Engen KJ. Completion norms for 3085 English sentence contexts.</p>

</div><!-- instructions -->

</div><!-- main -->


</body>
</html>

"""

f.write(longStr)



# close the file
f.close()
