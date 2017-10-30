from datetime import date, timedelta
import os
import sys
import trans

from medicover import Medicover


def notify(title, text):
    os.system(
        "osascript -e 'display notification \"{}\" with title \"{}\"'".format(text, title),
    )


def print_choices(m, region, specialization, clinic, doctor):
    choices = m.get_visit_parameters(region, specialization, clinic, doctor)
    choice_types = [  # name, required
        ('region', True),
        ('specialization', True),
        ('clinic', False),
        ('doctor', False),
    ]

    for name, required in choice_types:
        print('MEDICOVER_{}:'.format(name.upper()))
        lines = [
            '* {} [use code: {}]'.format(trans.trans(choice_value), choice_id)
            for choice_id, choice_value in choices[name].items()
            if not (required and choice_id < 0)
        ] or ['* Narrow down to see more options!']
        lines.sort()
        print('\n'.join(lines) + '\n')
    sys.exit(1)


if __name__ == '__main__':
    username = os.environ['MEDICOVER_USERNAME']
    password = os.environ['MEDICOVER_PASSWORD']

    region = int(os.environ.get('MEDICOVER_REGION', 0))
    specialization = int(os.environ.get('MEDICOVER_SPECIALIZATION', 0))
    clinic = int(os.environ.get('MEDICOVER_CLINIC', 0))
    doctor = int(os.environ.get('MEDICOVER_DOCTOR', 0))

    m = Medicover()

    with m.logged_in(username, password):
        if not (region and specialization and clinic and doctor):
            # Misconfiguration; die and print available options to the user.
            print('Application lacks configuration! Please set all environment variables:\n')
            print_choices(m, region, specialization, clinic, doctor)
            sys.exit(1)

        slots = m.get_free_slots(region, specialization, clinic, doctor)
        print(slots)
        today = date.today().isoformat()
        day_after_tomorrow = (date.today() + timedelta(days=2)).isoformat()
        for slot in slots['items']:
            slot_date = slot['appointmentDate']
            if today <= slot_date < day_after_tomorrow:
                text = "New slot available!\nDate:{}\nDoctor:{}".format(
                    slot_date, trans.trans(slot['doctorName'])
                )
                notify("Medicover", text)

