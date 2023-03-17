import sys
from datetime import datetime, timedelta
from pathlib import Path


def extract_name_birthday(path: Path) -> list:
    target_lst = []
    
    with open(path, 'r') as fn:
        lst = fn.readlines()
 
    for i in lst:
        dict_lst = {}
        i = i.strip()
        lst_i = i.split(':')
        lst_i[1] = datetime.strptime(lst_i[1], '%Y-%m-%d').date()
        dict_lst['name'] = lst_i[0]
        dict_lst['birthday'] = lst_i[1].replace(year=datetime.now().year)
        dict_lst['is_turning_years'] = dict_lst.get('birthday').year - lst_i[1].year
        target_lst.append(dict_lst)
        
    return target_lst

def create_target_dates() -> datetime.date:
    today = datetime.now().date()
    weekday = 7 - datetime.now().weekday()
    next_week_monday = today + timedelta(weekday)
    weekend = next_week_monday - timedelta(2)
    next_week_friday = next_week_monday + timedelta(4)

    return(weekend, next_week_monday, next_week_friday)
    
def search_birthdays(dates_lst: list) -> dict:
    weekend, next_week_monday, next_week_friday = create_target_dates()
    result = {}
    
    for member in dates_lst:
        if weekend <= member['birthday'] <= next_week_monday:
            try:
                result[next_week_monday] += f" {member['name']} turns {member['is_turning_years']}. "
            except KeyError:
                result[next_week_monday] = f" {member['name']} turns {member['is_turning_years']}. "
        if next_week_monday < member['birthday'] <= next_week_friday:
            try:
                result[member['birthday']] += f" {member['name']} turns {member['is_turning_years']}. "
            except KeyError:
                result[member['birthday']] = f" {member['name']} turns {member['is_turning_years']}. "     
    
    result = dict(sorted(result.items(), key=lambda x: x[0]))
    return(result)

def main():
    path = Path(sys.argv[1])
    employees = extract_name_birthday(path)
    result = search_birthdays(employees)

    for key, values in result.items():
        print(f"{key.strftime('%A')}:{values}")


if __name__ == "__main__":
    main()
