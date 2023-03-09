from ninja import Schema, ModelSchema
from targaryen.models import Person


class DragonOut(Schema):
    name: str
    birth_year: int


class PersonOut(ModelSchema):
    full_name: str

    class Config:
        model = Person
        model_fields = ["id", "birth_year", "name", "title"]

    @staticmethod
    def resolve_full_name(object):
        return f"{object.name} {object.title}"


class PersonIn(Schema):
    name: str
    title: str
    birth_year: int
