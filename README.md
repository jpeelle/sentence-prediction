# sentence-prediction

## About
This program takes two inputs:

1. A list of csv documents with Mechanical Turk data
2. A csv containing responses to be replaced and what to replace them with

It keeps track of all the answers given for each question and the frequency of those answers, replacing responses as required by the input csv. Replacements are an attempt to correct typos on the part of the participant, they are similar in nature to *"behive"* being replaced with *"beehive."* If the participant left the answer blank it was counted as  *"No Response."*

Once all answer are recorded a simple ratio of the number of times an answer was given over the total number of responses is calculated. The file *output.md* shows each question followed by the answers (from most common to least) and their decimal frequency.
