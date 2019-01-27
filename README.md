# sentence-prediction

## About

The goal of this project is to examine the predictability of sentence-final words using a cloze procedure. We created 3085 unique sentences; we then presented each sentence to an online participant without the last word, and asked them to provide the most likely response. For example,

He hated bees and feared encountering a _______________.

Common responses were "hive" and "beehive", but less common (and still appropriate) responses included "disease" or "yellowjacket". We count the frequency of each response to provide the likelihood of any given response as a proportion:

<pre>
1. He hated bees and feared encountering a __________.

        * hive (0.42)
        * swarm (0.20)
        * bee (0.09)
        * nest (0.08)
        * wasp (0.06)
        * beehive (0.05)
        * sting (0.04)
        * stinger (0.03)
        * hornet (0.02)
        * disease (0.01)
        * yellowjacket (0.01)
        * No Response (0.01)
</pre>


There are several programs:

1. `anonymizer.py` takes the original online data and anonymizes it by replacing unique user IDs with generated IDs. These IDs still correspond to individual respondents. We provide the anonymized data.

2. `predict_sent_analysis.py` which does the work of counting proportion of responses.



Mis-spellings or altered pluralization are a challenge. In our initial testing, automated approaches (e.g., using a dictionary) missed a large number of cases. Thus, we went through each response by hand and created a file of replacements that are completed prior to response frequencies being calculated. For example, "bee hive", "beehive", and "behive" were all counted as the same response. The replacements we made are in `replacements.csv`.

If the participant left the answer blank it was counted as  *"No Response."*

This program takes two inputs:

1. A list of csv files with Mechanical Turk data
2. A csv file containing responses to be replaced, and what to replace them with


## Dependencies

These scripts require Python 3.



## Outputs

Once all answer are recorded a simple ratio of the number of times an answer was given over the total number of responses is calculated. The file `output.md` shows each question followed by the answers (from most common to least) and their frequency as a proportion of all responses.


## Usage

To anonymize Mechanical Turk data, run: `$python3 anonymizer.py data_file_1 data_file_2 ...`. To count responses run: `$python predict_sent_analysis.py` with optional arguments `help` to print out a help message, `print` to print the output to the terminal, and `file` to write the output to a file named `output.md`. The current iteration will automatically use the anonymized data files and replacement file included in the example folder.


## Example data

The data provided in the `example` folder comprise 3085 sentences, for which we collected at least 100 responses online using Amazon Mechanical Turk.



