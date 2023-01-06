from typing import List, Dict

from user_api.database.models.user import User


def dict_to_select_query(table_name: str, dict_params: Dict) -> str:
    where_params = " WHERE "
    
    position = len(dict_params)
    for key, value in dict_params:
        s = key + " = " + "'" + value + "'" 
        where_params += s
        if position > 1:
            where_params += " AND "

    q = "SELECT * FROM " + table_name + where_params
    return q


def dict_to_count_query(table_name: str, dict_params: Dict) -> str:
    where_params = " WHERE "
    
    position = len(dict_params)
    for key, value in dict_params:
        s = key + " = " + "'" + value + "'" 
        where_params += s
        if position > 1:
            where_params += " AND "

    q = "SELECT COUNT(*) FROM " + table_name + where_params
    return q


def generate_user_models(raw_query_set: List[Dict]) -> List[User]:
    user_models = []

    for raw_user in raw_query_set:
        user = User(
            id=raw_user["id"],
            tg_id=raw_user["tg_id"],
            first_name=raw_user["first_name"],
            last_name=raw_user["last_name"],
            is_bot=raw_user["is_bot"],
            mailing_type=raw_user["mailing"],
            created_at=raw_user["created_at"],
            last_activity_date=raw_user["last_activity_date"],
            is_active=raw_user["is_active"],
            is_deleted=raw_user["is_deleted"],
        ) 
        user_models.append(user)
    
    return user_models


# TODO: refactor
def get_count_res(raw_data: List[Dict]) -> int:
    res = []

    for element in raw_data:
        for v in element.values():
            res.append(int(v))

    return res[0]
