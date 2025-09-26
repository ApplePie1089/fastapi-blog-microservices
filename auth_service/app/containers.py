from dependency_injector import containers
from dependency_injector.providers import Container, Singleton

from app import repositories


class Repositories(containers.DeclarativeContainer):
    tokens = Singleton(repositories.TokensRepository)
    users = Singleton(repositories.UsersRepository)


class Application(containers.DeclarativeContainer):
    repos = Container(Repositories)