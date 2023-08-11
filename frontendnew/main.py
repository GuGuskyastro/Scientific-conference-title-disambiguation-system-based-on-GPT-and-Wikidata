from nicegui import ui
from backend.main import Agent
from frontendnew.dict_edit import DictEdit
import yaml
import os


@ui.refreshable
async def generate() -> None:
    if os.path.exists('result.yaml'):
        with open('result.yaml', "r", encoding="utf-8") as test_data:
            test_data = yaml.safe_load(test_data)
    else:
        test_data = []

    with ui.row().classes('w-full items-center'):
        for i in range(0, len(test_data)):
            result = {'Citation Text': test_data[i]['Citation text'],
                      'Conference title': test_data[i]['Conference Info']['Conference title'],
                      'Conference short name': test_data[i]['Conference Info']['Conference short name'],
                      'Conference Qid': test_data[i]['Conference Info']['Conference Qid'],
                      'Conference startDate': test_data[i]['Conference Info']['Conference startDate'],
                      'Conference endDate': test_data[i]['Conference Info']['Conference endDate'],
                      'Conference location': test_data[i]['Conference Info']['Conference location'],
                      'WebSite': test_data[i]['Conference Info']['Conference officialWebsite']}
            with ui.column():
                card = ui.card()
                dict_edit = DictEdit(card, result)
                with ui.row():
                    if test_data[i]['Conference Info']['Conference officialWebsite'] != None:
                        with ui.link(target=test_data[i]['Conference Info']['Conference officialWebsite']):ui.button('Offical website')
                    else: ui.button('Offical website',on_click=lambda:ui.notify('Did not reach the official website in this Citation!'))

                    if test_data[i]['Conference Info']['Conference Qid'] != None:
                        with ui.link(target='https://www.wikidata.org/wiki/' + test_data[i]['Conference Info']['Conference Qid']):ui.button('Wikidata webpage')
                    else: ui.button('Offical website',on_click=lambda:ui.notify('Did not reach the Wikidata webpage in this Citation!'))

@ui.page('/')
async def main():

    async def send() -> None:
        user_input = text.value
        user_model = model_radio.value
        user_methode = methode_radio.value
        agent = Agent(model_name=user_model)

        if user_methode == 'Individually':
            Agent.generate_result(agent,user_input,show_token=True,use_integrate_agent=False)
        if user_methode == 'Intergrate':
            Agent.generate_result(agent, user_input, show_token=True, use_integrate_agent=True)

        generate.refresh()


    with ui.column().classes('w-full items-center'):
        ui.label('Conference Disambiguation System').style('color: #6E93D6; font-size: 200%; font-weight: 400')
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3').classes('w-full self-center')
            model_radio = ui.radio(['gpt-3.5-turbo', 'gpt-4'])
            methode_radio = ui.radio(['Individually', 'Intergrate'])
            ui.button('Start parsing', on_click=lambda: send())

        with ui.column().classes('w-full no-wrap items-center'):
            await generate()

ui.run()