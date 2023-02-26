from django.shortcuts import get_object_or_404
from targaryen.models import Person
from ninja import Router
from targaryen.schemas import DragonOut, PersonOut

router = Router()


@router.get("/dragons", response=list[DragonOut])
def dragons(request):
    data = [
        DragonOut(name="Drogon", birth_year=300),
        DragonOut(name="Rhaegal", birth_year=300),
    ]
    return data


@router.get("/person/{int:person_id}", response=PersonOut)
def person(request, person_id: int):
    return get_object_or_404(Person, id=person_id)
