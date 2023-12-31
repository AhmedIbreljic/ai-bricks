import sys; sys.path[0:0] = ['.','..'] # for local testing
from ai_bricks import agent
from ai_bricks.api import openai

model = openai.model('gpt-3.5-turbo', temperature=0.5) # key from OPENAI_KEY env variable

if 0:
	def log_state(kw, self):
		print('PROMPT', kw['messages'][1]['content'])
	model.add_callback('before', log_state)

agent.actions.VERBOSE_EXCEPTIONS = False
actions = {
	'wikipedia':              agent.actions.wikipedia_search_summaries,
	#'wikipedia-page-summary': agent.actions.wikipedia_summary,
	#'wikipedia-find-pages':   agent.actions.wikipedia_search,
	'python-eval':            agent.actions.python_eval,
}

#question = "What is the sum of square root of every third number from 123 to the year of the recent Russian invasion of Ukraine?"
#question = "Which moons in the solar system are bigger than Pluto?"
#question = "Whats on the news today? Check tvn24."
question = "Which planet has the biggest moon - Jupiter or Saturn?"


#print(agent.actions.wikipedia_search_summaries('Jupiter moons')); exit()

resp = agent.get('v2')(question, model=model, actions=actions, iter_limit=5)
print('agent response:', resp)
rtt_sum = sum(resp["rtt_list"])
cost_sum = sum(resp.get('cost_list',[]))
cnt = len(resp["rtt_list"])

print(f'\nDONE IN {rtt_sum:0.1f}s AND {cnt} steps ({rtt_sum/cnt:0.2f}s per step) FOR ${cost_sum:0.4f} ({model.name})')
print()
print('FINAL ANSWER:', resp['text'])
print()
