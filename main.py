from scraper import Property

HEADLESS = False


def main():

    P = Property('uc', headless2=HEADLESS, start=True)
    P.open_web()


if __name__ == '__main__':
    main()
