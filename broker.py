#!/usr/bin/env python3
# Off The Broker main file
# CLI tool that automates opt-out requests to databrokers via email

import smtplib
from email.message import EmailMessage
from textwrap import dedent
import os
import time
from dotenv import load_dotenv

# List of ANSI color codes

def blue(text: str) -> str:
    # Wrap text in ANSI codes for blue color
    return f"\033[34m{text}\033[0m"

def red(text: str) -> str:
    # Wrap text in ANSI codes for red color
    return f"\033[31m{text}\033[0m"

def green(text: str) -> str:
    # Wrap text in ANSI codes for green color
    return f"\033[32m{text}\033[0m"

def bold(text: str) -> str:
    # Wrap text in ANSI codes for bold
    return f"\033[1m{text}\033[0m"

dash = "-"
emptySpace = " "

def init():
    if os.path.exists(".env"):
        
        load_dotenv()
        
        # Email connection established
        SENDER_EMAIL = os.getenv("SENDER_EMAIL")
        PASSWORD = os.getenv("PASSWORD")

        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587

        # User info loaded from .env text file
        MY_FIRST_NAME = os.getenv("MY_FIRST_NAME")
        MY_LAST_NAME = os.getenv("MY_LAST_NAME")
        MY_EMAIL = os.getenv("MY_EMAIL")
        CITY = os.getenv("CITY")
        PROV = os.getenv("PROV")
        POST_CODE = os.getenv("POST_CODE")
        COUNTRY = os.getenv("COUNTRY")
        PHONE_NUM = os.getenv("PHONE_NUM")
        
        def UI_art():
            art = ["       _____   ",
                   "     _|_____|_ ",
                   "      | . . |  ",
                   "       \\___/  ",
                   "       /\\_/\\ "]
            for line in art:
                print(blue(line))

        def trademark(main):
            def wrapper():
                UI_art()
                print(blue(dash * 20))
                print(blue(bold((emptySpace * 3) + "Off The Broker")))
                print(blue(dash * 20))
                print(red("By: RavenTheBird789"))
                print(blue(dash * 20))
                print(blue(dash * 4) + blue("|") + (emptySpace * 2) + "v1.1.0" + (emptySpace * 2) + blue("|") + blue(dash * 4))
                print(blue(dash * 20))
                main()
            return wrapper
        
        def init_brokers():
            if os.path.exists("data_brokers.txt"):
                with open("data_brokers.txt", "r") as de:
                    return [line.strip() for line in de if line.strip()]
            return []

        def init_broker_names():
            if os.path.exists("brokers_names.txt"):
                with open("brokers_names.txt", "r") as dn:
                    return [line.strip() for line in dn if line.strip()]
            return []

        broker_emails = init_brokers()
        broker_names = init_broker_names()

        def init_emailed_brokers():
            if os.path.exists("emailed_brokers.txt"):
                with open("emailed_brokers.txt") as ebt:
                    return [line.strip() for line in ebt if line.strip()]
            return []

        def main_men_animation():
            os.system("cls" if os.name == "nt" else "clear")
            print(blue("Returning to the main menu" + "."))
            time.sleep(0.5)
            os.system("cls" if os.name == "nt" else "clear")
            print(blue("Returning to the main menu" + ("." * 2)))
            time.sleep(0.5)
            os.system("cls" if os.name == "nt" else "clear")
            print(blue("Returning to the main menu" + ("." * 3)))
            time.sleep(0.5)
            os.system("cls" if os.name == "nt" else "clear")

        def exit_animation():
            os.system("cls" if os.name == "nt" else "clear")
            print(blue("Exiting" + "."))
            time.sleep(0.5)
            os.system("cls" if os.name == "nt" else "clear")
            print(blue("Exiting" + ("." * 2)))
            time.sleep(0.5)
            os.system("cls" if os.name == "nt" else "clear")
            print(blue("Exiting" + ("." * 3)))
            time.sleep(0.5)
            os.system("cls" if os.name == "nt" else "clear")
            os._exit(0);

        DAILY_LIMIT = 150

        def build_email(name):
            return dedent(f"""\
                To whom it may concern at {name},

                I am writing to request that you delete all personal information you hold about me and opt me out of any sale, sharing, or disclosure of my personal information to third parties. Please also stop collecting, processing, and publishing my data going forward.

                To help you locate my records, my identifying details are:

                Name: {MY_FIRST_NAME} {MY_LAST_NAME}
                Email: {MY_EMAIL}
                Phone: {PHONE_NUM}
                Location: {CITY}, {PROV} {POST_CODE}, {COUNTRY}

                Depending on where I reside or resided, this request is made under applicable privacy laws, which may include:

                  - The California Consumer Privacy Act, as amended by the California Privacy Rights Act (Cal. Civ. Code § 1798.105, right to delete; § 1798.120, right to opt out of sale or sharing)
                  - The EU/UK General Data Protection Regulation (Article 17, right to erasure; Article 21, right to object)
                  - Any other applicable state, provincial, or national privacy laws

                Please also delete any data you obtained about me from other sources, and notify any third parties to whom you have sold or disclosed my information so they can do the same.

                Please confirm in writing once this request has been completed. Under the CCPA you have 45 days to respond (Cal. Civ. Code § 1798.130(a)(2)), and under the GDPR one month (Article 12(3)). If you need additional information to verify my identity, reply to this email, but please do not request more than is strictly necessary.

                Thank you for your prompt attention to this matter.

                Sincerely,
                {MY_FIRST_NAME} {MY_LAST_NAME}
                {SENDER_EMAIL}
                """)

        def opt_out():
            if len(broker_names) != len(broker_emails):
                print(red("brokers_names.txt and data_brokers.txt must have the same number of lines."))
                time.sleep(3)
                os.system("cls" if os.name == "nt" else "clear")
                main()
                return

            done = set(init_emailed_brokers())
            pending = [(n, e) for n, e in zip(broker_names, broker_emails) if e not in done]
            batch = pending[:DAILY_LIMIT]

            if not batch:
                print(blue("Every broker on your list has already been emailed."))
                time.sleep(3)
                os.system("cls" if os.name == "nt" else "clear")
                main()
                return

            sent_count = 0
            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(SENDER_EMAIL, PASSWORD)
                    for i, (name, email) in enumerate(batch, 1):
                        msg = EmailMessage()
                        msg["Subject"] = "Opt-out Request"
                        msg["From"] = SENDER_EMAIL
                        msg["To"] = email
                        msg.set_content(build_email(name))
                        try:
                            server.send_message(msg)
                        except smtplib.SMTPServerDisconnected:
                            print(red("Connection lost. Run again to continue where you left off."))
                            break
                        except smtplib.SMTPException as e:
                            print(red(f"{i}. Failed for {email}: {e}"))
                            continue
                        with open("emailed_brokers.txt", "a") as f:
                            f.write(email + "\n")
                        sent_count += 1
                        print(green(f"{i}. Sent to {email}"))
                        time.sleep(3)  # Prevent spam flag
            except KeyboardInterrupt:
                print(blue("\nStopped. Progress saved."))
            except smtplib.SMTPAuthenticationError:
                print(red("Login failed. Check your sender email and app password."))
            except (smtplib.SMTPException, OSError) as e:
                print(red(f"Could not connect to the mail server: {e}"))

            time.sleep(3)
            if sent_count == DAILY_LIMIT:
                print(blue("Daily limit reached.\nPlease come back again in 24 hours."))
            else:
                print(blue(f"Sent {sent_count} requests this run."))
            time.sleep(5)
            os.system("cls" if os.name == "nt" else "clear")
            main()

        def mod_data():
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            email_addr = input("Enter your email address: ")
            city = input("Enter your city of residence (current or prior): ")
            st_prov = input("Enter your state/province: ")
            post_code = input("Enter your postal/zip code: ")
            country = input("Enter your country: ")
            phone_num = input("Enter your phone number: ")
            sender_email = input("Enter the email you'll send the opt out requests from: ")
            app_pass = input("Enter your generated app password: ")
            with open(".env", "w") as ev:
                ev.write(f"MY_FIRST_NAME={first_name}\nMY_LAST_NAME={last_name}\nMY_EMAIL={email_addr}\nCITY={city}\nPROV={st_prov}\nPOST_CODE={post_code}\nCOUNTRY={country}\nPHONE_NUM={phone_num}\nSENDER_EMAIL={sender_email}\nPASSWORD={app_pass}")
            print(green("Your information has been updated successfully!"))
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            main();

        def nuke_data():
            prompt = input(blue("Are you sure you want to delete all your data?\nThis action cannot be reversed (y/n): ")).strip().lower()
            if prompt in ['y', 'yes']:
                if os.path.exists(".env"):
                    os.remove(".env")

                if os.path.exists("emailed_brokers.txt"):
                    os.remove("emailed_brokers.txt")

                os.system("cls" if os.name == "nt" else "clear")
                print(green("Your data has been deleted successfully"))
                time.sleep(2)
                os.system("cls" if os.name == "nt" else "clear")
                main();
            elif prompt in ['n', 'no']:
                main_men_animation()
                main();
            else:
                os.system("cls" if os.name == "nt" else "clear")
                print(red("Invalid Input"))
                time.sleep(2)
                os.system("cls" if os.name == "nt" else "clear")
                nuke_data();

        @trademark
        def main():
            print(blue("1. Send opt-out requests to different databrokers"))
            print(blue("2. Modify the data sent in your opt-out requests"))
            print(blue("3. Delete all your data"))
            print(blue("4. Exit"))
            query = input(blue("Please select an option from above (1-4): "))
            if query == "1":
                os.system("cls" if os.name == "nt" else "clear")
                opt_out()
            elif query == "2":
                os.system("cls" if os.name == "nt" else "clear")
                mod_data()
            elif query == "3":
                os.system("cls" if os.name == "nt" else "clear")
                nuke_data()
            elif query == "4":
                exit_animation()
            else:
                print(red("Invalid Input"))
                time.sleep(2)
                os.system("cls" if os.name == "nt" else "clear")
                main()
        main()
    else:
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email_addr = input("Enter your email address: ")
        city = input("Enter your city of residence (current or prior): ")
        st_prov = input("Enter your state/province: ")
        post_code = input("Enter your postal/zip code: ")
        country = input("Enter your country: ")
        phone_num = input("Enter your phone number: ")
        sender_email = input("Enter the email you'll send the opt out requests from: ")
        app_pass = input("Enter your generated app password: ")
        with open(".env", "w") as ev:
            ev.write(f"MY_FIRST_NAME={first_name}\nMY_LAST_NAME={last_name}\nMY_EMAIL={email_addr}\nCITY={city}\nPROV={st_prov}\nPOST_CODE={post_code}\nCOUNTRY={country}\nPHONE_NUM={phone_num}\nSENDER_EMAIL={sender_email}\nPASSWORD={app_pass}")
        os.system("cls" if os.name == "nt" else "clear")
        init()
init()
