from pydantic import BaseModel

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

class VelovPairConclusion(BaseModel):
    from_station: int
    to_station: int
    from_station_name: str
    to_station_name: str
    from_station_bikes: int = -1
    from_station_elec: bool = False
    from_station_mec: bool = False
    to_station_stands: int = -1
    journey_status: str = "no"


def prepare_velov_data(data: dict, pairs: [(int, int)]):
    conclusions = []
    
    for pair in pairs:
        station_from = pair[0]
        station_to = pair[1]

        from_data = [d for d in data['values'] if d['number'] == station_from]
        from_data = from_data[0] if len(from_data) > 0 else None 

        to_data = [d for d in data['values'] if d['number'] == station_to]
        to_data = to_data[0] if len(to_data) > 0 else None

        if from_data == None or to_data == None:
            continue

        conclusion = VelovPairConclusion(
            from_station=station_from, 
            to_station=station_to,
            from_station_name=from_data["name"],
            to_station_name=to_data["name"]
            )

        if from_data["total_stands"]["availabilities"]["electricalBikes"] > 0:
            conclusion.from_station_elec = True

        if from_data["total_stands"]["availabilities"]["mechanicalBikes"] > 0:
            conclusion.from_station_mec = True

        conclusion.from_station_bikes = from_data["total_stands"]["availabilities"]["bikes"]
        conclusion.to_station_stands = to_data["total_stands"]["availabilities"]["stands"]

        if conclusion.to_station_stands > 2 and conclusion.from_station_bikes > 2:
            conclusion.journey_status = "ok"
        elif conclusion.to_station_stands > 0 and conclusion.from_station_bikes > 0:
            conclusion.journey_status = "warn"

        conclusions.append(conclusion)

    return conclusions