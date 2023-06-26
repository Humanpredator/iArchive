import os
import pickle
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect


def get_cookiefile():
    default_cookiefile = {
        "Windows":
        "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin":
        "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit(
            "No Cookies Found For Instagram. Please Login Your IG on Firefox...!"
        )
    return cookiefiles[0]


def import_session():
    cookiefile = get_cookiefile()
    print("Using cookies from {}.".format(cookiefile))
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cursor = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
        cookie_data = cursor.fetchall()
    except OperationalError:
        cursor = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )
        cookie_data = cursor.fetchall()

    filename = "./sessionfile"

    with open(filename, "wb") as file:
        cookies_dict = dict(cookie_data)
        pickle.dump(cookies_dict, file)

    print("Session File Have Been Stored To: ".format(filename))


if __name__ == "__main__":
    if os.path.exists("./sessionfile"):
        os.remove("./sessionfile")
        print("Existing Session File Have Been Removed...!")
    import_session()
