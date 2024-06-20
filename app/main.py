from dependency_injector.wiring import inject, Provide
from dotenv import load_dotenv
from app.api.api_handler import APIHandler
from app.container import Container


@inject
def main(api_handler: APIHandler = Provide[Container.api_handler]):
    return api_handler.app


load_dotenv()
container = Container()
container.init_resources()
container.wire(modules=[__name__])
app = main()
