import re
import json

lst = json.loads(input())
bus_id, stop_type, stop_name, a_time = [], [], [], []

for t in lst:
    bus_id += [t['bus_id']]
    stop_type += [t['stop_type']]
    stop_name += [t['stop_name']]
    a_time += [t['a_time']]


def check_field():
    field_type = {
        # 'bus_id': 0,
        # 'stop_id': 0,
        'stop_name': 0,
        # 'next_stop': 0,
        'stop_type': 0,
        'a_time': 0
    }
    for item in lst:
        for k, v in item.items():
            if k == 'stop_name' and not re.match(r'([A-Z][a-z]+ )+(Road|Street|Avenue|Boulevard)$', v):
                field_type[k] += 1
            if k == 'stop_type' and not re.match(r'[SOF]$', v) and v != '':
                field_type[k] += 1
            # if k in ['bus_id', 'stop_id', 'next_stop'] and not isinstance(v, int):
            #     field_type[k] += 1
            if k == 'a_time' and not re.match(r'([01]\d|2[0-4]):[0-5]\d$', v):
                field_type[k] += 1

    err = sum(field_type.values())
    print(f'Format validation: {err} errors')
    for i in field_type.items():
        print(f'{i[0]}: {i[1]}')


def count_stops():
    stop_count = {}
    for i in lst:
        for k, v in i.items():
            try:
                if k == 'bus_id':
                    stop_count[v] += 1
            except KeyError:
                stop_count[v] = 1
    print(stop_count)


def check_point():
    bus_stops = {}
    for b, s in zip(bus_id, stop_type):
        try:
            bus_stops[b] += s
        except KeyError:
            bus_stops[b] = s

    for k, v in bus_stops.items():
        if not re.match('SO*F', v):
            return print(f'There is no start or end stop for the line: {k}.')

    trans = {}
    for n, i in zip(stop_name, bus_id):
        try:
            trans[n].append(str(i))
        except KeyError:
            trans[n] = [str(i)]
    transfer_stops = [k for k, v in trans.items() if len(v) > 1]

    start_stops = []
    finish_stops = []
    for stops, names in zip(stop_type, stop_name):
        if stops == 'S':
            start_stops.append(names)
        if stops == 'F':
            finish_stops.append(names)

    # print('Start stops: ', len(start_stops), sorted(start_stops))
    # print('Transfer stops: ', len(transfer_stops), sorted(transfer_stops))
    # print('Finish stops: ', len(set(finish_stops)), sorted(set(finish_stops)))

    return transfer_stops


def check_time():
    time_set = {}
    for b, a, s in zip(bus_id, a_time, stop_name):
        try:
            time_set[b].append((a, s))
        except KeyError:
            time_set[b] = [(a, s)]
    wrong_time = []
    print('Arrival time test:')
    for k, v in time_set.items():
        for i, j in enumerate(v[:-1]):
            if j[0] > v[i+1][0]:
                wrong_time.append(k)
                print(f'bus_id line {k}: wrong time on station {v[i+1][1]}')
                break
    if not wrong_time:
        print('OK')


def check_on_demand():
    trans = check_point()
    check_lst = {}
    for n, k in zip(stop_name, stop_type):
        try:
            check_lst[n] += k
        except KeyError:
            check_lst[n] = k
    wrong_lst = []
    for k, v in check_lst.items():
        if re.match('SO|OF', v) or (v == 'O' and k in trans):
            wrong_lst.append(k)
    print('On demand stops test:')
    print('Wrong stop type:', sorted(wrong_lst) if wrong_lst else 'OK')


check_on_demand()
