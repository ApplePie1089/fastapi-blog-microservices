from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Container

from app import repositories


class Repositories(DeclarativeContainer):
    users_repository = Singleton(repositories.UsersRepository)


class Application(DeclarativeContainer):
    repos = Container(Repositories)