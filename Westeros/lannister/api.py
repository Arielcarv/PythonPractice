from ninja import Router

router = Router()


@router.get("/home")
def home(request):
    return "A lannister always pays their debts"


@router.get("/rock")
def rock(request, height:int):
    return f"Casterly Rock is {height + 1}m tall"
