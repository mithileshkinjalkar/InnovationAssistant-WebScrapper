from dotenv import set_key, dotenv_values
from collections import deque
from datetime import datetime
from WebScraper import extract_urls, scrape_urls
from LLMInteractions import generate_summary, tag_industries, tag_resource_types
from ExportHTML import export_to_html


# Function handling the application interface and processing for its first/clean run
def first_run(airtable, records):
    """
        Params:
            --airtable: Airtable object representing the base table
            --records: List of tuples with data
        Return:
            --None
                Setup Airtable and run through summary generation along with HTML formating.
    """

    print("\nScraping web links and generating summaries...\n")

    # Accessing Airtable records, scraping the retrieved URLs and storing the scraped text in the Airtable base
    urls = extract_urls(records)
    scraped_text = scrape_urls(urls)
    airtable.write_to_airtable(scraped_text, field="Scraped Data")

    # Generating summaries based on the scraped text and stroing the generated summaries in the Airtable base
    summaries = generate_summary(scraped_text)
    airtable.write_to_airtable(summaries, field="Short Program Summary")

    # Tagging each summary with it's relevant industry and storing the industry tags in the Airtable base
    industries = tag_industries(summaries)
    airtable.write_to_airtable(industries, field="Industry")

    # Tagging each summary with it's relevant resource type and storing the resource type tags in the Airtable base
    resource_types = tag_resource_types(summaries)
    airtable.write_to_airtable(resource_types, field="Resource Type")

    # Update record count
    records = airtable.integrate_airtable()
    set_key(dotenv_path="../.env", key_to_set="RECORD_COUNT", value_to_set=str(len(records)))


# Function to handle the menu interface and make appropriate process calls as per user input
def menu(airtable):
    """
        Params:
            --airtable: Airtable object representing the base table
        Return:
            --choice: The integer value of the menu option chosen by the user
                Display menu listing application utilities.
    """

    print("\nSelect an option:\n\t1. Update Airtable\n\t2. Export Data to HTML\n\t3. Reset Airtable\n\t4. Exit")

    # 'choice' value of '4' indicates application termination
    # It triggers breaking out of the interface loop
    while True:
        choice = input("\nChoice: ")
        try:
            choice = int(choice)
            records = airtable.integrate_airtable()
            if choice == 1:
                config = dotenv_values("../.env")
                record_count = int(config["RECORD_COUNT"])

                # Check record count and update if necessary
                # The below code aims to find the latest records (count of records to find equals the offset value)
                if len(records) > record_count:
                    offset = len(records) - record_count
                    offset_records = deque()
                    latest_created = None
                    for record in records:
                        created = datetime.strptime(record["fields"]["Created"][:10], "%Y-%m-%d").date()
                        if latest_created is None: 
                            latest_created = created
                            offset_records.append(record)
                        else:
                            if created >= latest_created: 
                                latest_created = created
                                if len(offset_records) < offset: offset_records.append(record)
                                else:
                                    offset_records.popleft()
                                    offset_records.append(record)

                    # Once the additional records are identified a clean run with only those records is initiated
                    first_run(airtable, list(offset_records))
                    # .env file is updated with the new record count
                    set_key(dotenv_path="../.env", key_to_set="RECORD_COUNT", value_to_set=str(len(records)))
                
                print("Airtable successfully updated!")
            elif choice == 2:
                # Export data to raw HTML
                export_to_html(records)
            elif choice == 3: 
                # Reset or refresh the programmatic Airtable view
                first_run(airtable, records)
                print("System reset successful!")
            elif choice == 4: pass # Exit from the application
            else: raise ValueError
        except ValueError: print("Invalid choice, try again.")
        else: return choice
