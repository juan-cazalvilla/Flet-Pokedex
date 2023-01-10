import flet
import aiohttp, asyncio
from functools import partial

api_url = "http://minimalapi-pokedex.azurewebsites.net"

async def api_call(session, call):
    async with session.get(call) as response:
        return await response.json()

async def get_all_pokemon():
    async with aiohttp.ClientSession() as session:
        call = api_url + "/pokedex/all"
        result = await api_call(session, call)
    return result

async def get_data_pokemon(name):
    async with aiohttp.ClientSession() as session:
        call = api_url + f"/pokedex/{name}"
        return await api_call(session, call)

def open_data(pokemon_name):
    data = asyncio.run(get_data_pokemon(pokemon_name))
    return data

def main(page: flet.Page):
    page.title = "Flet pokedex example"
    page.bgcolor = flet.colors.BLUE_GREY_200
    pokemon_list = asyncio.run(get_all_pokemon())

    def close_dlg(e):
        page.dialog.open = False
        page.update()

    def create_dialog(pokemon_name):
        data = open_data(pokemon_name)['variations'][0]
        return flet.AlertDialog(
            modal=True,
            title=flet.Text(pokemon_name),
            content = flet.Column([
                flet.Image(
                            src = f"http://minimalapi-pokedex.azurewebsites.net/{data['image']}",
                            width = 150,
                            height = 200,
                            fit = flet.ImageFit.FILL
                        ),
                flet.Text(f"Description: {data['description']}"),
                flet.Text("Type: " + " ".join(data['types'])),
                flet.Text(f"Specie: {data['specie']}"),
                flet.Text("Evolutions: \n" + "\n".join(data['evolutions'])),
                ]
            ),

            actions=[
                flet.TextButton("Back", on_click=close_dlg),
            ],
            actions_alignment=flet.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    def open_dlg_modal(e, data):
        dlg_modal = create_dialog(data)
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    grid = flet.GridView(
        expand=1,
        runs_count=4,
        max_extent=200,
        child_aspect_ratio=0.60,
        spacing=4,
        run_spacing=5,
    )

    for item in pokemon_list['data']:
        grid.controls.append(
            flet.Card(
                elevation = 5,
                content = flet.Container(
                    on_click = partial(open_dlg_modal, data=f"{item['name']}"),
                    width = 150,
                    height = 200,
                    padding = 10,
                    bgcolor = flet.colors.WHITE,
                    content = flet.Column([
                        flet.Image(
                            src = f"http://minimalapi-pokedex.azurewebsites.net/{item['image']}",
                            width = 150,
                            height = 200,
                            fit = flet.ImageFit.FILL
                        ),
                        flet.Text(f"{item['name']}")
                    ]
                    )
                )
            )
        )

    page.add(grid)


flet.app(target=main, view = flet.WEB_BROWSER)