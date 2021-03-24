def copy_volunteers():
    from .models import Action, ActionAssignedVolunteers, ActionFeedback
    for a in Action.objects.all():
        if a.assigned_volunteer:
            a.assigned_volunteers.add(a.assigned_volunteer)

def copy_feedback():
    from .models import ActionFeedback, ActionAssignedVolunteers
    for af in ActionFeedback.objects.all():
        av, created = ActionAssignedVolunteers.objects.update_or_create(
            action=af.action,
            assigned_volunteer=af.volunteer)
        af.assigned_volunteer_action=av
        af.save()