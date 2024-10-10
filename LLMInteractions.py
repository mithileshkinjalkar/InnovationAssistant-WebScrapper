from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tqdm import tqdm

def init_llm(max_tokens=None):
    """
        Params:
            --max_tokens: The maximum number of tokens expected in the model's response

        Return:
            --llm: Instantiated LLM object
    """

    llm = ChatOpenAI(
        name="gpt-4o-mini",
        temperature=0,
        max_tokens=max_tokens
    )

    return llm


def generate_summary(scraped_text):
    """
        Params:
            --scraped_text: List of tuples comprising of the scraped HTML content along with Airtable record ID

        Return:
            --summaries: List of tuples comprising of the generated summary for each resource
              along with the corresponding Airtable record ID
    """
    summaries = list()

    llm = init_llm(max_tokens=500)
    parser = StrOutputParser()

    system_template = """
        You are a helpful text summarization assistant. You will be provided with scraped HTML data. You need to respond with a 4-5 sentence (300-400 words) summary. The generated summary must be in third person. Extract the key themes from the text and highlight it in the summary.
    """.strip()
    messages = [
        ("system", system_template),
        ("user", "HTML Data: {html_content}\nSummary:")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | llm | parser

    for html_content, id in tqdm(scraped_text,
                                 desc="Generating Summaries", 
                                 ncols=100,
                                 unit="resource",
                                 colour="#35e48f"):
        summary = chain.invoke({"html_content": html_content})
        summaries.append((summary, id))
    
    print()
    return summaries


def tag_industries(summaries):
    """
        Params:
            --summaries: List of tuples comprising of summaries and corresponding Airtable record ID

        Return:
            --industries: List of tuples comprising the relevant industry and Airtbale record ID
    """
    industries = list()

    llm = init_llm()
    parser = StrOutputParser()

    system_template = """
        You are a helpful text tagging assistant. You will be provided with short summaries. You need to tag each summary appropriately using the below list of industries. A single tag is to be returned for each summary.

        Tags:
        Agriculture
        AI / Machine Learning
        Alternative Medicine
        Architecture / Planning
        Automation / Robotics
        Aviation / Aerospace
        Biotechnology / Greentech
        Broadcast Media
        Chemical
        Civic / Social Organization
        Cleantech
        Computer Hardware
        Computer / Network Security
        Construction
        Consumer Goods & Services
        Cosmetics
        Defense / Space
        Diagnostic
        Education & E-Learning
        Entertainment / Movie Production
        Events Services
        Finance / Investment Technologies
        Financial Services
        Food & Beverage
        Government Agency
        Government Relations
        Graphic Design / Web Design
        Hardware / Engineering Technologies
        Health / Fitness
        Higher Education / Academia
        Hospital / Health Care
        Hospitality
        Human Resources / HR
        Information / Technology Services
        International Trade / Development
        Investment Banking / Venture
        Law Practice / Law Firms
        Legislative Office
        Life Science
        Manufacturing / Materials
        Marketing / Advertising / Sales
        Mass Media
        Mechanical or Industrial Engineering
        Medical Device Technologies
        Mental Health Care
        Military / Defense
        Nanotechnology
        Newspapers / Journalism
        Non-Profit Organization
        Oil / Energy / Solar / Greentech
        Pharmaceuticals / Therapeutics
        Philanthropy
        Primary / Secondary Education
        Public Safety
        Recreational Facilities / Services
        Renewables / Environment
        Research Tools
        Restaurants
        Retail / E-commerce
        Semiconductors
        Software Technologies
        Sports / E-sports
        Telecommunications
        Transportation & Utilities
        Venture Capital / VC
        Veterinary
        Water & Blue Technologies
        Wireless
    """.strip()
    messages = [
        ("system", system_template),
        ("user", "Summary: {summary}\nIndustry Tag:")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | llm | parser

    for summary, id in tqdm(summaries,
                            desc="Tagging industries", 
                            ncols=100,
                            unit="resource",
                            colour="#35e48f"):
        industry = chain.invoke({"summary": summary})
        industries.append((industry, id))
    
    print()
    return industries


def tag_resource_types(summaries):
    """
        Params:
            --summaries: List of tuples comprising of summaries and corresponding Airtable record ID

        Return:
            --resource_types: List of tuples comprising the relevant resource type and Airtbale record ID
    """
    resource_types = list()

    llm = init_llm()
    parser = StrOutputParser()

    system_template = """
        You are a helpful text tagging assistant. You will be provided with short summaries. You need to tag each summary appropriately using the below list of resource types. A single tag is to be returned for each summary. Only include the tag and do not include the number identifying the tag.

        Resources Types:
        Accelerator
        Incubator
        Networking Resource
        Legal Resource
        Education Resource
        Entrepreneurship & Innovation Event
        Student Program
        Funding & Investor Resource
    """.strip()
    messages = [
        ("system", system_template),
        ("user", "Summary: {summary}\nResource Type Tag:")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | llm | parser

    for summary, id in tqdm(summaries,
                            desc="Tagging resource types", 
                            ncols=100,
                            unit="resource",
                            colour="#35e48f"):
        resource_type = chain.invoke({"summary": summary})
        resource_types.append((resource_type, id))
    
    print()
    return resource_types
