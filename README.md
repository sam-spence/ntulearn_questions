# ntulearn_questions
Convert quiz questions from text to tab-delimited format for NTULearn.
If you like to write your NTULearn questions in Word, and then you copy-paste them 1,000 times into Excel to get a tab-delimited file, then stop doing that. Use this program instead.

The current version will handle these question types:
- MC Multiple choice
- MA Multiple answer
- TF True or false
- SR Short response
- ORD Ordering
- MAT Matching

It will not yet do:
- Fill in the blank
- Multiple fill in the blank
- Essay 
- Jumbled sentence
- Numeric response
- Opinion scale
- Quiz bowl


# Writing your questions in Word #

Write your questions in Word and save as a UTF-8 .txt file (not .docx). You just need to add some codes to the questions for the program to recognise the questions and answers.

\%\% The question should start with double percent signs. After the %%, put the type of question, e.g. %%MC1 for multiple choice. The question number is optional.
\@\@ Each option that can be picked should start with doulbe at signs.
\>\> The correct answer(s) should start with double greater than signs.
\#\# Any comments on the question, e.g. how to work out the answer, should be surrounded by double hashes. Comments won't be included in the output. ##

Examples:

```\%\%MC1 Which fruit smells bad?
\@\@A apple
\@\@B banana
\@\@C cherry
\@\@D durian
\>\> D
\#\# Multiple choice. Just give the one correct answer after the >> \##

\%\%MA2 Which fruits are edible?
\@\@A apple
\@\@B banana
\@\@C cherry
\@\@D durian
\>\> A
\>\> B
\>\> C
\#\# Multiple answer. Give all the correct answers, each with a >> ##

\%\%TF3 Durian is safe to eat.
\>\> False
\#\# True or false. Just give true or false after >> ##

\%\%SR4 Write a short response descrbing the aroma of durian.
\#\# Short response. No >> answers needed, just give the question. ##

\%\%ORD5 Arrange the durians from smallest to biggest.
\>\> 10cm
\>\> 20cm
\>\> 30cm
\#\# Ordering. Give all answers in the correct order. They will be randomised by NTULearn. ##

\%\%MAT6 Match the fruit to the adjective that describes its taste.
\@\@ apple
\>\> refreshing
\@\@ cherry
\>\> elegant
\@\@ durian
\>\> abhorrent
\#\# Matching. Give each option with its corresponding answer underneath. They will be scrambled by NTULearn. ##```


# Using the program #

The short version:

```ntuLearnQuestions.py <input file path>```

The output tab-delimited file will be created in the same folder as the input, with the same name, ending with \_tab_format.txt.


The long version:

Windows:


Mac and Linux:

