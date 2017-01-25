import fractions

def any_correct(given_answers, correct_answers):
    '''Returns true if ANY of the given answers are correct, given the correct answers'''

    for correct in correct_answers:
        for given in given_answers:
            if is_correct(given, correct):
                return True
    return False

def all_correct(given_answers, correct_answers):
    '''Returns true if ALL of the given answers are correct, given the correct answers'''

    # First, check if all correct answers were given
    for correct in correct_answers:
        if not any_correct(given_answers, [correct]):
            return False

    # Second, check if all given answers are correct
    for given in given_answers:
        if not any_correct(correct_answers, [given]):
            return False

    return True

def convert_to_number(answer):
    '''Tries to convert the supplied answer to a numeric value. Raises ValueError on failure.'''

    # remove whitespace
    answer = "".join(answer.split())

    # replace comma's (it's a dutch thing...)
    answer = answer.replace(',','.')

    try:
        return int(answer)
    except ValueError:
        try:
            return float(answer)
        except ValueError:
            return float(fractions.Fraction(answer))

def is_correct(given_answer, correct_answer):
    '''Returns whether the given answer is correct, given the correct answer. Correct answers can be strings, numbers, or numbers in GIFT notation (low..high or answer:tolerance)'''

    try:
        numeric_given_answer = convert_to_number(given_answer)
    except ValueError:
        numeric_given_answer = None

    try:
        numeric_correct_answer = convert_to_number(correct_answer)
        return numeric_given_answer == numeric_correct_answer
    except ValueError:
        pass

    try:
        parts = correct_answer.split('..')
        lower_limit = convert_to_number(parts[0])
        upper_limit = convert_to_number(parts[1])
        return numeric_given_answer and lower_limit <= numeric_given_answer <= upper_limit
    except (ValueError, IndexError):
        pass

    try:
        parts = correct_answer.split(':')
        mean = convert_to_number(parts[0])
        tolerance = convert_to_number(parts[1])
        lower_limit = mean - tolerance
        upper_limit = mean + tolerance
        return numeric_given_answer and lower_limit <= numeric_given_answer <= upper_limit
    except (ValueError, IndexError):
        pass

    string_given_answer = ''.join(filter(str.isalnum, given_answer.lower()))
    string_correct_answer = ''.join(filter(str.isalnum, correct_answer.lower()))
    return string_given_answer == string_correct_answer
