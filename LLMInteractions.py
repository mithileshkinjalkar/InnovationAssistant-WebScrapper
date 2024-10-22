from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tqdm import tqdm

# Function to initialize the LLM
def init_llm(max_tokens=None):
    """
        Params:
            --max_tokens: The maximum number of tokens expected in the model's response

        Return:
            --llm: Instantiated LLM object
    """

    # We opted for 'gpt-4o-mini' because of cheaper usage charges
    llm = ChatOpenAI(
        name="gpt-4o-mini",
        temperature=0,
        max_tokens=max_tokens
    )

    return llm


# Function to prompt the integrated LLM for generating
# summaries of the scraped raw HTML for each URL in the Airtable
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
        You are a helpful text summarization assistant. You will be provided with HTML data. You need to respond with a 4-5 sentence (300-400 words) summary. The generated summary must be strictly in third person. The response should not mention references to the HTML data or text used to generate the summary. Additionally, it should not explicitly mention the term summary. Extract the key themes from the text and highlight it in the summary.

        Example of the type of summary response to avoid: "The HTML data pertains to Prof. Kelly Goldsmith and her work in marketing research, focusing on videos, slides, research best practices, and analytics. The content also includes bonus material related to these topics. Prof. Goldsmith's expertise in these areas is highlighted through the provided information."
        
        Example of the type of summary response expected: "Prof. Kelly Goldsmith is a recognized expert in marketing research, focusing on practical applications of marketing principles. Her educational resources, including videos and slides, provide valuable insights into research best practices, equipping learners with the tools necessary to navigate the complexities of the marketing landscape. Goldsmith emphasizes the importance of data-driven decision-making, as reflected in her "Analytics in Action" series, which demonstrates how analytics can be applied to solve real-world marketing problems. Additionally, she offers supplementary materials to further enhance understanding and provide a deeper dive into advanced marketing concepts. Her work aims to foster a thorough comprehension of marketing research and analytics for both students and professionals."
    """.strip()
    messages = [
        ("system", system_template),
        ("user", "HTML Data: {html_content}\nSummary:")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    # The chain will first build a prompt using the 'System' and 'User' messages
    # This prompt will be fed to the LLM
    # The parser will help to extract the response text from the LLM response
    chain = prompt | llm | parser

    for html_content, id in tqdm(scraped_text,
                                 desc="Generating Summaries", 
                                 ncols=100,
                                 unit="resource",
                                 colour="#35e48f"):
        summary = chain.invoke({"html_content": html_content}) # Invoke the chain for each URL
        summaries.append((summary, id)) # ID is again retained for Airtable writing purpose
    
    print()
    return summaries


# Function to tag each summary with its appropriate industry
# Highlighting which industry each resource belongs to
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


# Function to classify/tag each resource by its type
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
        You are a helpful text tagging assistant. You will be provided with short summaries. You need to tag each summary appropriately using the below list of resource types. A single tag is to be returned for each summary.

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
