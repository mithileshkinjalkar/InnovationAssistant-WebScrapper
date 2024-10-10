from collections import defaultdict
from tqdm import tqdm
import os
import time

def delete_files_in_dir(dir_path):
    """
        Params:
            --dir_path: Relative/Absolute path to the directory from which all files need to be deleted
        Return:
            --None
                Delete all files from the specified directory path
    """
    try:
        with os.scandir(dir_path) as files:
            for file in files:
                if file.is_file(): os.unlink(file.path)
            print(f"\nAll exported files deleted. Directory has been cleared.")
    except OSError:
        print(f"\nError in deleting files. Delete manually if necessary (Path: <project_path>/exports).")

def export_to_html(records):
    """
        Params:
            --records: Dictionary representing the project's Airtable base
        Return:
            --None
                Though, export raw HTML in a .txt file
    """

    extracted_info = list()

    for record in records:
        fields = record["fields"]
        if fields["UCSD?"] == 'no':
            if "Resource Name" in fields.keys() and\
                "Link" in fields.keys() and\
                "Short Program Summary" in fields.keys() and\
                "Industry" in fields.keys() and\
                "Resource Type" in fields.keys():
                extracted_info.append(
                    (fields["Resource Name"],
                     fields["Link"],
                     fields["Short Program Summary"],
                     fields["Industry"],
                     fields["Resource Type"])
                )
    
    html = "<h2><strong>Other Resources</strong></h2>\n"
    
    res_type_mappings = defaultdict(list)
    for info in extracted_info:
        resource, link, summary, industry, res_type = info
        res_type_mappings[res_type].append((resource, link, summary, industry))

    for res_type in res_type_mappings:
        html += f"<h3><strong>{res_type}</strong></h3>\n"
        for info in res_type_mappings[res_type]:
            resource, link, summary, industry = info
            html += f"""<p><strong>{resource}</strong> (<a href=\"{link}\">{link}</a>)</p>
            <p>{summary}</p>
            <p><strong>Industry: </strong><span></span>{industry}</p>
            <p></p>
            
            """
    
    MAX_FILE_COUNT = 5
    file_count = 0
    relative_dir_path = "exports"
    for item in os.scandir(relative_dir_path):
        if item.is_file():
            file_count += 1
        if file_count == MAX_FILE_COUNT:
            print(f"\nMaximum allowable file count ({MAX_FILE_COUNT}) reached. Clearing directory...")
            delete_files_in_dir(relative_dir_path)
        
    filename = f"OtherResources_{time.strftime("%m-%d-%Y_%H%M%S")}.txt"
    with open(f"exports/{filename}", 'w') as file:
        file.write(html)
    
    print(f"\nSuccessfully exported content to HTML!")
