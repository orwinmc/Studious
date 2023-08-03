import os
import dotenv
import PyPDF2 as pypdf
import openai
from collections import namedtuple
import json
from tqdm import tqdm

SAMPLE_PDF = 'Pharmacodynamics II_Hillard_Slides.pdf'
SAMPLE_PDF2 = 'RML_2023_FOM_Translation_TNP_finalaudio.pdf'

Flashcard = namedtuple('Flashcard', ['front', 'back'])

def get_mock_response(filename):
	with open('./mocking/' + filename, 'r') as json_file:
		return json.load(json_file)

def convert_response_to_flashcards(response):
	chat_content = response['choices'][0]['message']['content']
	flashcard_contents = chat_content.split("*Question*:")[1:]

	flashcards = []
	for flashcard_content in flashcard_contents:
		front, back = flashcard_content.split("\n*Answer*:")
		flashcards.append(Flashcard(front,back[:-2])) # Remove newlines

	return flashcards


def load_prompt(filename):
	with open(filename,"r") as file:
		return ''.join(file.readlines())

def setup():
	dotenv.load_dotenv()

	openai.api_key = os.getenv('CHATGPT_API_KEY')

	reader = pypdf.PdfReader('./samples/inputs/pdfs/' + SAMPLE_PDF2)

	prompt = load_prompt("./prompts/note_taking_prompt.txt")

	return reader, prompt

def write_flashcards_to_csv(filename):
	with open(filename, 'w') as file:
		file.write("front,back\n")
		for card in flashcards:
			file.write('"' + card.front + '","' + card.back + '"\n')

if __name__ == '__main__':
	reader, prompt = setup()

	flashcards = []

	for i,page in tqdm(enumerate(reader.pages)):
		slide_content = page.extract_text()

		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=[{"role": "user", "content": prompt + '\n' + slide_content}]
		)

		#response = get_mock_response('mock_response.json')

		flashcards += convert_response_to_flashcards(response)

	write_flashcards_to_csv('samples/outputs/' + SAMPLE_PDF2[:-3] + '.csv')

