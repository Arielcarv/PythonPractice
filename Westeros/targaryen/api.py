from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router

from targaryen.models import Person
from targaryen.schemas import DragonOut, PersonOut, PersonIn

router = Router()


@router.get("/dragons", response=list[DragonOut])
def dragons(request):
    data = [
        DragonOut(name="Drogon", birth_year=300),
        DragonOut(name="Rhaegal", birth_year=300),
    ]
    return data


@router.get("/person/", response=list[PersonOut])
def list_person(request):
    queryset = Person.objects.all()
    return queryset


@router.get("/person/{int:person_id}", response=PersonOut)
def person(request, person_id: int):
    return get_object_or_404(Person, id=person_id)


@router.post("/person/")
def create_person(request, person: PersonIn):
    person_object = Person.objects.create(**person.dict())
    person_dict = model_to_dict(person_object)
    return person_dict
