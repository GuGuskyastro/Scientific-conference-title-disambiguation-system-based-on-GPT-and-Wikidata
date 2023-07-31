from typing import List, Tuple
from nicegui import Client, ui
from backend.main import Agent

# The page constructed by this code shows a simple interactive system, base on the dialog example from nicegui.
agent = Agent()
messages: List[Tuple[str, str]] = []


@ui.refreshable
async def chat_messages() -> None:
    for name, text in messages:
        ui.chat_message(text=text, name=name, sent=name == 'You')


@ui.page('/')
async def main(client: Client):
    async def send() -> None:
        message = text.value
        messages.append(('You', message))
        response = Agent.run(agent,message)
        messages.append(('GPT', response))
        chat_messages.refresh()

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')
    await client.connected()

    with ui.column().classes('w-full items-center'):
        ui.label('Conference Disambiguation System').style('color: #6E93D6; font-size: 200%; font-weight: 400')


    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        await chat_messages()

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
            ui.button('Start parsing', on_click=lambda: send())


ui.run()