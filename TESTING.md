Testing plan
===

Create a volunteer
---

### Action

 Create a volunteer in the admin (has "Enhanced DBS Check")

### Expected

- New entry in the admin listing
- Email received with invite link

### Action

 Open invite link **in separate browser** and set a password

### Expected

- Automatically logged in
- No access to co-ordinator view

Second profile
---

### Action

 Create Coordinator, picking the user of the Volunteer profile

### Expected

- New entry in Coordinator listing
- **No** email sent with an invite

Synchronisation
---

### Action

 Update information on one of the profiles

### Expected

- Information is updated on the other profile
- Information is updated on the user account

Second volunteer
---

### Action

 Create and finalized account for a second volunteer ("Enhanced DBS Check" + "Dog walking experience")

### Expected

 Same as first volunteer

Update action types
---

### Action

- Set the "Dog walk" action type to require "Dog walking experience"
- Set the "Prescription" action to have some template

### Expected

 Entries are updated

> TODO: Test new action types are visible to all volunteers? Test icon update?

Create resident
---

### Action

 Create resident

### Expected

 New resident in the listing

Create actions
---

### Action

 Create a "Dog Walk" action for today 18:00, high priority.

### Expected

- It should automatically get the "Dog walking experience" requirement
- Only the person that has "Dog walking experience" should receive an email

### Action

 Create a "Shopping" action for tomorrow 18:00, high priority, with private description.

### Expected

- Both volunteers should get an email

### Action

 Create a "Prescription" action for tomorrow 18:00, normal priority

### Expected

- It should automatically have the description filled with template content

> TODO: Test filtering on wards (still a thing?) & help preferences, not just requirement

Action listing for volunteers
---

### Action

 Look at listing of action from both volunteers account

### Expected

- Only volunteer with Dog Walk experience should see the dog walk action
- Actions should be ordered chronologically, then by priority

Volunteering
---

### Action

 Volunteer for "Shopping" action with both volunteer

### Expected

- The private description of the action does not appear
- Action should have moved to the "Upcoming" list, in the "Awaiting approval" section
- Both volunteer should have a hand emoji on the admin

Assign to one of the volunteers
---

### Action

 Assign to one of the volunteers

### Expected

- "Assigned on" should get filled on the action
- For chosen volunteer:
- Action is listed out of the "Awaiting approval" section
- Selected volunteer sees private inform
- Email received to let them know they have more info
- For other volunteer:
- If on the action page already, refreshing shows "Sorry, someone is already on it"
- Action is no longer listed
- Email received to let them know it's not on

Complete job
---

### Action

 Complete the job with the assigned volunteer

### Expected

- Contact date is set
- Feedback is registered with the information from the form
- Action is moved to the "Complete" list

Second action
---

### Action

 Register interest to another job with the assigned volunteer, assign to them

### Expected

- A star appears next to the volunteer's name in the admin when assigning

Mark action as ongoing
---

### Action

 Complete action, ticking the "this action" will be ongoing

### Expected

- Action details show the "Ongoing" options at the footer

Fill in some feedback
---

### Action

 Add a couple of feedback from the volunteer

### Expected

- Feedbacks get saved in the admin

- Times are tallied for the action, volunteer and resident

TODO: Test tally is updated when removing feedback

Complete ongoing action
---

### Action

 Notify admin that ongoing action is complete

### Expected

- Final feedback is registered
- Action has moved to "Complete" list
