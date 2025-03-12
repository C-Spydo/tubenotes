from langchain.prompts import ChatPromptTemplate

def get_prompt_templates():
    positive_impact = get_positive_impact_template()
    potential_issues = get_potential_issues_template()
    cold_mail = get_cold_email_template()
    email_title= get_email_title_generation_template()

    return positive_impact, potential_issues, cold_mail, email_title

def get_positive_impact_template():
    return ChatPromptTemplate.from_messages([
        ('system', 'You are a business developement assistant for an insurance firm, '
                   'mention points to emphasize to get the attention of a prospective cutomer in any industry '
                   '(e.g a procpect in the financial industry would be attracted by how insurance can help with security and ROI).'
                   'simply, list do not explain.'),
        ('user',  'give me 3 areas to emphasize in a cold mail for a prospective customer in the {industry} industry')
    ])

def get_potential_issues_template():
    return ChatPromptTemplate.from_messages([
        ('system', 'You are a business developement assistant for an insurance firm, '
                'mention potential issues againt insurance to counter to get the attention of a prospective cutomer in any industry.'
                'Simply, list do not explain.'),
        ('user',  'give me 3 ill feelings to counter in a cold mail for a prospective customer in the {industry} industry')
    ])

def get_cold_email_template():
    return ChatPromptTemplate.from_messages([
        ('system', 'You are a business developement assistant for Icecebreaker insurance firm, '
                    'tackling the following potential issues againt insurance \n {potential_issues}\n'
                    'And emphasizing the following positive impacts:\n {positive_impact}\n'
                    'Assume that this email will be forwarded directly, and do not give me instructions in it'),
        ('user',   'Curate a concise cold mail body (no subject) to get the attention of a prospective cutomer named {name} in the {industry} industry.'
                    'The mail is to be sent by the Icebreaker Business Development team')
    ])

def get_email_title_generation_template():
    return ChatPromptTemplate.from_messages([
        ('system', 'You are an assistant'),
        ('user',   'Give a concise and catchy email title to this mail: \n{email}\n'
                   'Just the title, no follow-up or explanatory text!')
    ])

