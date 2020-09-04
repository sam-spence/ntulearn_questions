#!/usr/bin/env python3 

# Convert text file of questions into a tsv file for upload to NTU Learn

import argparse
import csv
import os
import re
import traceback 

def parseTextQuestion(problem): # Take text string of a question and return a tsv line for the question
		
	# Multiple choice question
	if problem.startswith('MC'):
		if not '@@' in problem:
			raise Exception('No options starting with @@ found.')
		if not '>>' in problem:
			raise Exception('No answers starting with >> found.')
		questionText = re.search(r'^MC(?:\d+)?\.?([\s\S]*?)(?=@@)', problem).group(1) # Text describing the problem
		question = questionText.replace('\n', ' ')
		question = question.strip()
		choiceTexts = re.findall(r'^@@[^\n]+', problem, re.M) # Options for student to choose ['@@A 1', '@@B 2', '@@C 3', '@@D 4']
		answerText = re.search(r'^>>[^\n]+', problem, re.M).group() # The correct answer '>> A'
		answer = answerText.strip('>>').strip() # 'A'
		answers = [choice.startswith('@@' + answer) for choice in choiceTexts] # [True, False, False, False]
		answers = ['correct' if answer == True else 'incorrect' for answer in answers]  # ['correct', 'incorrect', 'incorrect', 'incorrect']
		choices = [re.sub(r'^@@[a-zA-Z]+\s', '', choice).strip() for choice in choiceTexts] # ['1', '2', '3', '4']
		tsvRow = ['MC', question]
		for i in range(len(choices)):
			tsvRow.append(choices[i])
			tsvRow.append(answers[i])
		return(tsvRow)
	
	# Multiple answer question
	elif problem.startswith('MA') and not problem.startswith('MAT'):
		if not '@@' in problem:
			raise Exception('No options starting with @@ found.')
		if not '>>' in problem:
			raise Exception('No answers starting with >> found.')
		questionText = re.search(r'^MA(?:\d+)?\.?([\s\S]*?)(?=@@)', problem).group(1) # Text describing the problem
		question = questionText.replace('\n', ' ')
		question = question.strip()
		choiceTexts = re.findall(r'^@@[^\n]+', problem, re.M) # Options for student to choose ['@@A 1', '@@B 2', '@@C 3', '@@D 4']
		answerTexts = re.findall(r'^>>[^\n]+', problem, re.M) # The correct answers ['>> A', '>> C']
		answerTexts = [answer.strip('>>').strip(' ') for answer in answerTexts] # ['A', 'C']
		choiceCodes = [re.search(r'^@@([a-zA-Z]+)', choice).group(1) for choice in choiceTexts] # ['A', 'B', 'C', 'D']
		answerCodes = [None for choice in choiceTexts] # ['correct', 'correct', 'incorrect', 'incorrect']
		for i in range(len(answerCodes)):
			if choiceCodes[i] in answerTexts:
				answerCodes[i] = 'correct'
			else:
				answerCodes[i] = 'incorrect'
		choices = [re.sub(r'^@@[a-zA-Z]+\s', '', choice).strip() for choice in choiceTexts] # ['1', '2', '3', '4']
		tsvRow = ['MA', question]
		for i in range(len(choices)):
			tsvRow.append(choices[i])
			tsvRow.append(answerCodes[i])
		return(tsvRow)

	# True or false question
	elif problem.startswith('TF'):
		if not '>>' in problem:
			raise Exception('No true/false answer starting with >> found.')
		questionText = re.search(r'^TF(?:\d+)?\.?([\s\S]*?)(?=>>)', problem).group(1) # Text describing the problem
		question = questionText.replace('\n', ' ')
		question = question.strip()
		answerText = re.search(r'^>>[^\n]+', problem, re.M).group() # The correct answer '>> false'
		answer = answerText.strip('>>').strip() # 'false'
		answer = answer.lower()
		if not answer in ['true', 'false']:
			raise Exception('The answer needs to be \'true\' or \'false\'.')
		tsvRow = ['TF', question, answer]
		return(tsvRow)

	# Short reply question
	elif problem.startswith('SR'):
		questionText = re.search(r'^SR(?:\d+)?\.?(.*)', problem).group(1) # Text describing the problem
		question = questionText.replace('\n', ' ')
		question = question.strip()
		tsvRow = ['SR', question]
		return(tsvRow)

	# Ordering question
	elif problem.startswith('ORD'):
		if not '>>' in problem:
			raise Exception('No answers starting with >> found.')
		questionText = re.search(r'^ORD(?:\d+)?\.?([\s\S]*?)(?=>>)', problem).group(1) # Text describing the problem
		question = questionText.replace('\n', ' ')
		question = question.strip()
		answerTexts = re.findall(r'^>>[^\n]+', problem, re.M) # The answers in the correct order ['>> A', '>> B', '>> C']
		answers = [answer.strip('>>').strip() for answer in answerTexts]
		tsvRow = ['ORD', question]
		for answer in answers:
			tsvRow.append(answer)
		return(tsvRow)

	# Matching question
	elif problem.startswith('MAT'):
		if not '@@' in problem:
			raise Exception('No options starting with @@ found.')
		if not '>>' in problem:
			raise Exception('No answers starting with >> found.')
		questionText = re.search(r'^MAT(?:\d+)?\.?([\s\S]*?)(?=@@)', problem).group(1) # Text describing the problem
		question = questionText.replace('\n', ' ')
		question = question.strip()
		choiceTexts = re.findall(r'^@@[^\n]+', problem, re.M) # Options for students to find matches for ['@@ 1', '@@ 2', '@@ 3', '@@ 4']
		answerTexts = re.findall(r'^>>[^\n]+', problem, re.M) # Answers for student to match with options ['>> 1', '>> 2', '>> 3', '>> 4']
		if len(choiceTexts) != len(answerTexts):
			raise Exception('Number of choices with @@ does not equal number of answers with >>.')
		choices = [choice.strip('@@').strip() for choice in choiceTexts]
		answers = [answer.strip('>>').strip() for answer in answerTexts]
		tsvRow = ['MAT', question]
		for i in range(len(choices)):
			tsvRow.append(choices[i])
			tsvRow.append(answers[i])
		return(tsvRow)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Converts a text file of questions into tsv format for uploading to NTU Learn.')
	parser.add_argument('inFile', metavar='input_file', help='Path to the input text file containing the questions.')
	args = parser.parse_args()
	
	with open(args.inFile, 'r') as file:
		fileText = file.read()
	fileText = fileText.replace('“','"').replace('”','"').replace('’', '\'') # Remove curly quotes
	problems = fileText.split('%%') # List of problems in the assignment
	problems = [re.sub(r'##[\s\S]*?##', '', problem) for problem in problems] # Remove comments from questions
	outputRows = [] # List of tab separated rows that will be sent to the output file
	for i, problem in enumerate(problems):
		try:
			outputRows.append(parseTextQuestion(problem)) # Make a tsv row for this question and add it to the list of rows
		except Exception as e:
			print('Error parsing question %s...' % problem[1:100])
			print(e)
			traceback.print_exc()
			print('\n')
			outputRows.append('\n') # Make a blank row for the missing question
	outputRows = [row for row in outputRows if row != None]
	outFile = os.path.splitext(args.inFile)[0] + '_tab_format.txt'
	with open(outFile, 'w') as out:
		writer = csv.writer(out, delimiter='\t')
		writer.writerows(outputRows)
	print('\nWrote formatted problems to %s.' % outFile)


	## To-do:

	## Handle smart quotes instead of replacing

	## Fill in the blank

	## Multiple fill in the blank

	## Essay 

	## Jumbled sentence

	## Numeric response

	## Opinion scale

	## Quiz bowl
