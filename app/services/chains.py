from langchain_groq import ChatGroq
from langchain_core.runnables.base import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from .prompt_template import get_prompt_templates

def get_cold_mail_chain():
    positive_impact_extracting_chain, potential_issues_extracting_chain, email_creation_chain, email_title_generating_chain = get_sub_chains()

    chain = (
        RunnableParallel(
            branches={
                'positive_impact': positive_impact_extracting_chain, 
                'potential_issues': potential_issues_extracting_chain, 
                'industry': RunnableLambda(lambda x: x['industry'])
            }
        )|
        RunnableLambda(
            lambda x: {
                'positive_impact': x['branches']['positive_impact'], 
                'potential_issues': x['branches']['potential_issues'], 
                'industry': x['branches']['industry']
            }
        )| email_creation_chain | 
        RunnableParallel(
            branches={
                'email': RunnableLambda(lambda x: x),
                'title': email_title_generating_chain
            }
        )|
        RunnableLambda(
            lambda x: {"title": x['branches']['title'] , "email": x['branches']['email']}
        )
    )

    return chain

def get_sub_chains():
    llm = get_llm()

    remove_white_spaces = RunnableLambda(lambda x: " ".join(x.split()))

    positive_impact_template, potential_issues_template, cold_mail_template, email_title_template = get_prompt_templates()

    positive_impact_extracting_chain = positive_impact_template | llm | StrOutputParser() | remove_white_spaces
    potential_issues_extracting_chain = potential_issues_template | llm | StrOutputParser() | remove_white_spaces
    email_creation_chain = cold_mail_template | llm | StrOutputParser()
    email_title_generating_chain = email_title_template | llm | StrOutputParser()   

    return positive_impact_extracting_chain, potential_issues_extracting_chain, email_creation_chain, email_title_generating_chain

def get_llm():
    return ChatGroq(
            model="llama3-8b-8192",
            temperature=0.6,
            max_tokens=None,
            timeout=3,
            max_retries=2
    )
