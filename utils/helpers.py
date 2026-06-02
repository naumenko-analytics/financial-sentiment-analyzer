from datetime import datetime

def format_date(date_str):
    """ Function that converts date string to a readable format
    """
    try:
        date = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return datetime.strftime("%B %d, %Y")
    except:
        return date_str
    
def truncate_text(text, max_length = 200):
    """ Function that truncates texts
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'

def validate_company_input(company):
    """ Function that validates user input for a company name
    """
    if not company or not company.strip():
        return False, "Please enter a company name."
    if len(company.strip()) < 2:
        return False, "Company name too short."
    if len(company.strip()) > 100:
        return False, "Company name too long"
    return True, ""