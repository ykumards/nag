from datetime import datetime, timedelta

def parse_date(input_date):
    """Parse the input date string or relative date (e.g., 'yesterday') and return a date string."""
    today = datetime.now()

    # Handle relative dates
    if input_date == "today":
        return today.strftime("%Y-%m-%d")
    elif input_date == "yesterday":
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif input_date == "tomorrow":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")

    # Handle specific dates in MM/DD or DD/MM format
    try:
        parsed_date = datetime.strptime(input_date, "%m/%d/%Y")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        try:
            parsed_date = datetime.strptime(input_date, "%m/%d")
            return parsed_date.replace(year=today.year).strftime("%Y-%m-%d")
        except ValueError:
            return None