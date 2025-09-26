from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Container

from app import repositories


class Repositories(DeclarativeContainer):
    categories_repository = Singleton(repositories.CategoriesRepository)
    posts_repository = Singleton(repositories.PostsRepository)


class Application(DeclarativeContainer):
    repos = Container(Repositories)