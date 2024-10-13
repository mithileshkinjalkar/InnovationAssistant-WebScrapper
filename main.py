from dotenv import dotenv_values, load_dotenv
load_dotenv() # Load environment variables from the .env file

from AirtableIntegration import Airtable
from ExportHTML import export_to_html
from AppRun import first_run, menu
from pyfiglet import figlet_format

def main():
    config = dotenv_values("../.env")
    
    # Airtable Initialization
    baseId, tableId, authToken = config["AIRTABLE_BASE_ID"], config["AIRTABLE_TABLE_ID"], config["AIRTABLE_ACCESS_TOKEN"]
    airtable = Airtable(baseId, tableId, authToken)

    print(figlet_format("Innovation Assistant Scraper", font="speed"))
    print("=======================================================================\n")

    # Main loop for creating an interactive, user-facing application
    while True:
        response = input("Using the Scraper for the first time? (Y/N) ").lower()
        if response == 'yes' or response == 'y':
            records = airtable.integrate_airtable()
            first_run(airtable, records)
            
            # Exporting data to HTML format in a .txt file
            while True:
                response = input("Would you like to export the generated data to raw HTML? (Y/N) ").lower()
                if response == 'yes' or response == 'y':
                    records = airtable.integrate_airtable()
                    export_to_html(records)
                    break
                elif response == 'no' or response == 'n': break
                else: print("Incorrect response, try again.\n")
            while True:
                response = input("\nDo you wish to continue? (Y/N) ").lower()
                if response == 'yes' or response == 'y':
                    choice = menu(airtable)
                    if choice == 4: break # 'choice' value of '4' implies termination of the application
                elif response == 'no' or response == 'n': break
                else: print("Incorrect response, try again.\n")

            break
        elif response == 'no' or response == 'n': 
            choice = menu(airtable)

            if choice != 4:
                while True:
                    response = input("\nDo you wish to continue? (Y/N) ").lower()
                    if response == 'yes' or response == 'y':
                        choice = menu(airtable)
                        if choice == 4: break
                    elif response == 'no' or response == 'n': break
                    else: print("Incorrect response, try again.\n")

            break
        else: print("Incorrect response, try again.\n") 
    
    print(figlet_format("Thank you for using!", font="rectangles"))

if __name__ == "__main__":
    main()
