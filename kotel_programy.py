#variable entity
climate_entity = 'climate.kotel'
temp_entity = 'sensor.ble_temperature_teplomer' #unimportant
heater_entity = 'switch.relay'
prog_switch = 'input_select.program_termostatu' #create it in helpers

#get actual target temperature
act_target_temp = hass.states.get(climate_entity).attributes['temperature'] 

#get actual  temperature in room
#act_temp = hass.states.get(temp_entity).attributes['temperature'] 

#get selected temp program
sel_prog = hass.states.get(prog_switch).state

#get datetime
now = datetime.datetime.now().time()


#Programs
RANNI_PROGRAM = [
    [datetime.time( 0, 0), datetime.time( 2, 59), 19], # from 00:00 to 02:59, temperature 19
    [datetime.time( 3, 0), datetime.time( 4, 59), 22],
    [datetime.time( 5, 0), datetime.time(16, 59), 19],
    [datetime.time(17, 0), datetime.time(20, 59), 22],
    [datetime.time(21, 0), datetime.time(23, 59), 19]
]
NOCNI_PROGRAM = [
    [datetime.time( 0, 0), datetime.time( 4, 59), 19],
    [datetime.time( 5, 0), datetime.time( 7, 59), 22],
    [datetime.time( 8, 0), datetime.time(12, 59), 20],
    [datetime.time(13, 0), datetime.time(16, 59), 22],
    [datetime.time(17, 0), datetime.time(23, 59), 19]
]
DOMA_PROGRAM = [
    [datetime.time( 0, 0), datetime.time( 6, 59), 19],
    [datetime.time( 7, 0), datetime.time( 20, 59), 22],
    [datetime.time(21, 0), datetime.time(23, 59), 19]
]

automat = False

if sel_prog == 'Doma':
    current_program = DOMA_PROGRAM
    automat = True
if sel_prog == 'Ranní':
    current_program = RANNI_PROGRAM
    automat = True
if sel_prog == 'Noční':
    current_program = NOCNI_PROGRAM
    automat = True
if sel_prog == 'Manuál':
    new_target_temp = act_target_temp

if automat == True:   
    for get_time_temp in current_program:
        start = get_time_temp[0]
        end = get_time_temp[1]
        temp = get_time_temp[2]
    
        if start <= now <= end:        
            new_target_temp = get_time_temp[2]
            break

    
    
#set new temperature
if act_target_temp != new_target_temp:
    hass.services.call('climate', 'set_temperature', {'entity_id': climate_entity, 'temperature': new_target_temp})
