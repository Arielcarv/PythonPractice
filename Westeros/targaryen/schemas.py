from ninja import Schema, ModelSchema
from targaryen.models import Person


class DragonOut(Schema):
    name: str
    birth_year: int


class PersonOut(ModelSchema):
    class Config:
        model = Person
        model_fields = ["id", "birth_year", ]

    @staticmethod
    def resolve_full_name(object):
        return f"{object.name} {object.title}"
