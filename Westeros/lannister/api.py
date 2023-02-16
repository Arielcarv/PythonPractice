from ninja import Router

router = Router()


@router.get("/home")
def home(request):
    return "A lannister always pays their debts"
