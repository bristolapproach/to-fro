def copy_volunteers():
    from .models import Action
    for a in Action.objects.all():
        if a.assigned_volunteer:
            a.assigned_volunteers.add(a.assigned_volunteer)

def copy_feedback():
    pass