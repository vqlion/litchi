def prepare_tcl_data(data: dict, stop_ids_to_name: dict):
    '''
    returns a dict: line -> dict of stops -> dict of directions -> list of passage times
    '''
    res = {}
    for value in data['values']:
        line = value['ligne']
        direction = value['direction']
        arrive_time = value['heurepassage']
        stop_id = value['id']
        stop_name = stop_ids_to_name[stop_id] if stop_id in stop_ids_to_name else stop_id

        if not line in res:
            res[line] = {stop_name: {direction: [arrive_time]}}
        elif not stop_name in res[line]:
            res[line][stop_name] = {direction: [arrive_time]}
        elif not direction in res[line][stop_name]:
            res[line][stop_name][direction] = [arrive_time]            
        else:
            res[line][stop_name][direction].append(arrive_time)

    for _, directions in res.items():
        for _, stops in directions.items():    
            for _, times in stops.items():
                times.sort()

    return res

def get_stop_names_from_tcl_data(data: dict):
    '''
    returns a dict: stop_id -> stop name
    '''

    res = {}
    for value in data['values']:
        stop_id = value['id']
        stop_name = value['nom']
        res[stop_id] = stop_name

    return res