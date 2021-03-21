def copy_volunteers():
    from .models import Action, ActionVolunteers, ActionFeedback
    for a in Action.objects.all():
        for v in a.interested_volunteers.all():
            av, created = ActionVolunteers.objects.update_or_create(
                action=a,
                volunteer=v,
                defaults={'interested': True}
            )
        if a.assigned_volunteer:
            av, created = ActionVolunteers.objects.update_or_create(
                action=a,
                volunteer = a.assigned_volunteer,
                defaults={'assigned': True}
            )

def copy_feedback():
    from .models import ActionFeedback, ActionVolunteers
    for af in ActionFeedback.objects.all():
        av, created = ActionVolunteers.objects.update_or_create(
            action=af.action,
            volunteer=af.volunteer)
        af.action_volunteer=av
        af.save()
