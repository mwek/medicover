import os
import trans

from medicover import Medicover


def notify(title, text):
    os.system(
        "osascript -e 'display notification \"{}\" with title \"{}\"'".format(text, title),
    )


if __name__ == '__main__':
    username = os.environ['MEDICOVER_USERNAME']
    password = os.environ['MEDICOVER_PASSWORD']

    m = Medicover()
    with m.logged_in(username, password):
        appointments = m.get_free_slots()
        print(appointments)
        for appointment in appointments['items']:
            appt_date = appointment['appointmentDate']
            if '2017-10-23' <= appt_date < '2017-10-25':
                text = "New appointment available!\nDate:{}\nDoctor:{}".format(
                    appt_date, trans.trans(appointment['doctorName'])
                )
                notify("Medicover", text)

