import sys
import math

def calc_wiz_dest_coor(wiz_x, wiz_y, wiz_vx, wiz_vy, snaffle_x, snaffle_y, snaffle_vx, snaffle_vy):
    alfa = math.atan2(snaffle_y + snaffle_vy - (wiz_y + wiz_vy), snaffle_x + snaffle_vx - (wiz_x + wiz_vx))
    dest_x = (int)(math.cos(alfa) * 500 + wiz_x)
    dest_y = (int)(math.sin(alfa) * 500 + wiz_y)
    return dest_x, dest_y

def calc_throw_vector(wiz_x, wiz_y, wiz_vx, wiz_vy, dest_x, dest_y, snaffle_thrust):

    for rounds_iter in range(10):

        rounds = rounds_iter * 2 + 1
        # Calculate snuffle initial impulse vector direction and distance towards destination after round
        alfa = math.atan2(dest_y - (wiz_y + wiz_vy*(1-0.75**rounds)/(1-0.75)), dest_x - (wiz_x + wiz_vx*(1-0.75**rounds)/(1-0.75)))
        distance_to_dest = math.sqrt((dest_y - (wiz_y + wiz_vy*(1-0.75**rounds)/(1-0.75)))**2 + (dest_x - (wiz_x + wiz_vx*(1-0.75**rounds)/(1-0.75)))**2)
    
        # Calculate required thurst vector direction after round to reach destination
        norm_x = math.cos(alfa)
        norm_y = math.sin(alfa)
    
        # calculate thurst vector impact to direction after rounds
        snaffle_vx = norm_x * snaffle_thrust * (1-0.75**rounds)/(1-0.75)
        snaffle_vy = norm_y * snaffle_thrust * (1-0.75**rounds)/(1-0.75)
    
        # calculate how much thurst would have taken snuffle closer towards destination
        thurst_distance_correction_to_dest = math.sqrt(snaffle_vx**2 + snaffle_vx**2)
    
        # if thurst would have been enough to reach destination, save thurst vector direction and calculate throw coordinates for throw command and return values
        if rounds_iter > 1:
            throw_x = (int)((norm_x + previous_round_norm_x)/2 * 500 + wiz_x)
            throw_y = (int)((norm_y + previous_round_norm_y)/2 * 500 + wiz_y)
            snaffle_v = math.sqrt(math.pow(wiz_vx + (norm_x + previous_round_norm_x)/2 * snaffle_thrust,2) + math.pow(wiz_vy + (norm_y + previous_round_norm_y)/2 * snaffle_thrust, 2))
            distance_to_dest = math.sqrt(math.pow(dest_x - wiz_x ,2) + math.pow(dest_y - wiz_y, 2))
        else:
            throw_x = (int)(norm_x * 500 + wiz_x)
            throw_y = (int)(norm_y * 500 + wiz_y)
            snaffle_v = math.sqrt(math.pow(wiz_vx + norm_x * snaffle_thrust,2) + math.pow(wiz_vy + norm_y * snaffle_thrust, 2))
            distance_to_dest = math.sqrt(math.pow(dest_x - wiz_x ,2) + math.pow(dest_y - wiz_y, 2))
        # calculate the snaffle actual speed taking into account initial impulse and thurst combined impact
        
        previous_round_norm_x = norm_x
        previous_round_norm_y = norm_y  
        if thurst_distance_correction_to_dest >= distance_to_dest:
            break 
        
    
    return throw_x, throw_y, snaffle_v, distance_to_dest  
    

def object_in_front_of_line(x0, y0, x1, y1, x2, y2, radius_power_2):
    if ((x0 > x1) and (x2 > x1)) or ((x2 < x1) and (x0 < x1)):
        result = (math.pow((y2-y1)*x0-(x2-x1)*y0 + x2*y1-y2*x1, 2)) / ((math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)))
        if result <= radius_power_2:
            return 1
    return 0


def main():
    my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
    
    # game loop
    turn = 0
    opponent_goal = {'state': 0, 'goal_x': 0, 'goal_y': 0}
    my_goal = {'state': 0, 'goal_x': 0, 'goal_y': 0}
    bludger_attack = {'state' : 0, 'entity_id' : 0, 'opponent_id' : 0}
    
    snaffle_radius = 150
    snaffle_radius2 = math.pow((snaffle_radius + snaffle_radius), 2)
    wizard_radius = 400
    wizard_radius2 = math.pow((wizard_radius + snaffle_radius), 2)
    opponent_wizard_radius = 400
    opponent_wizard_radius2 = math.pow((wizard_radius + snaffle_radius), 2)
    bludger_radius = 200
    bludger_radius2 = math.pow((bludger_radius + snaffle_radius), 2)
    
    
    goal_target_points_real = []
    goal_target_points_real_up = []
    goal_target_points_real_down = []
    n_points = 3
    
    goal_start_real_up = -5563
    goal_end_real_up = -1939
    
    goal_start_real = 1938
    goal_end_real = 5562
    
    goal_start_real_down = 9439
    goal_end_real_down =13063
    
    goal_width = goal_end_real - goal_start_real
    goal_width_up = goal_end_real_up - goal_start_real_up
    goal_width_down = goal_end_real_down - goal_start_real_down
    
    count = 0
    while count < n_points:
        goal_target_points_real.append((int)(goal_start_real + (goal_width / n_points) * (count) + 0.5 * (goal_width / n_points)))
        goal_target_points_real.append((int)(goal_start_real_up + (goal_width_up / n_points) * (count) + 0.5 * (goal_width_up / n_points)))
        goal_target_points_real.append((int)(goal_start_real_down + (goal_width_down / n_points) * (count) + 0.5 * (goal_width_down / n_points)))
        count+=
    
    while True:
        turn += 1
        my_score, my_magic = [int(i) for i in input().split()]
        opponent_score, opponent_magic = [int(i) for i in input().split()]
        entities = int(input())  # number of entities still in game
        
        wizard = []
        opponent_wizard = []
        snaffle = []
        bludger = []
        
        goal_warning = {'state': 0, 'entity_id': 0, 'x': 0}
        goal_score = {'state': 0, 'entity_id': 0, 'x': 0}
        
        
        for i in range(entities):
            entity_id, entity_type, x, y, vx, vy, state = input().split()
            entity_id = int(entity_id)
            x = int(x)
            y = int(y)
            vx = int(vx)
            vy = int(vy)
            state = int(state)
            if (entity_type == "WIZARD"):
                wizard.append({'entity_id': entity_id, 'entity_type': entity_type, 'x': x, 'y': y, 'vx': vx, 'vy': vy, 'state': state})
                if turn == 1:  
                    # I'm on the left 
                    if x < 5000:
                        opponent_goal['goal_x'] = 16000
                        opponent_goal['goal_y'] = 3750
                        opponent_goal['state'] = 0
                        my_goal['goal_x'] = 0
                        my_goal['goal_y'] = 3750
                        my_goal['state'] = 1
                    # I'm on the right
                    else:
                        opponent_goal['goal_x'] = 0
                        opponent_goal['goal_y'] = 3750
                        opponent_goal['state'] = 1
                        my_goal['goal_x'] = 16000
                        my_goal['goal_y'] = 3750
                        my_goal['state'] = 0
                    
            if (entity_type == "OPPONENT_WIZARD"):
                opponent_wizard.append({'entity_id': entity_id, 'entity_type': entity_type, 'x': x, 'y': y, 'vx': vx, 'vy': vy, 'state': state})
            if (entity_type == "SNAFFLE"):
                snaffle.append({'entity_id': entity_id, 'entity_type': entity_type, 'x': x, 'y': y, 'vx': vx, 'vy': vy, 'state': state})
                # NOTE: goal['state']  LEFT= 0, RIGHT= 1
                # IF checks if the snaffle is close (< 1000 m) to MY goal depending weather it's right/left
                
                if (opponent_goal['state'] == 0 and x < 2000) or (opponent_goal['state'] == 1 and x > 15000):
                    if (opponent_goal['state'] == 0 and x < 2000) and (goal_warning['state'] == 1 and x < goal_warning['x']):
                        goal_warning['state'] = 1
                        goal_warning['entity_id'] = entity_id
                        goal_warning['x'] = x
                    elif (opponent_goal['state'] == 1 and x > 15000) and (goal_warning['state'] == 1 and x > goal_warning['x']):
                        goal_warning['state'] = 1
                        goal_warning['entity_id'] = entity_id
                        goal_warning['x'] = x
                    else:
                        goal_warning['state'] = 1
                        goal_warning['entity_id'] = entity_id
                        goal_warning['x'] = x

                # IF checks if the snaffle is close (< 1000 m ) to OPPONENT goal depending weather it's rigth/left
                if (my_goal['state'] == 0 and x < 3000) or (my_goal['state'] == 1 and x > 13000):
                    if (my_goal['state'] == 0 and x < 2000) and (goal_score['state'] == 1 and x < goal_score['x']):
                        goal_score['state'] = 1
                        goal_score['entity_id'] = entity_id
                        goal_score['x'] = x
                    elif (my_goal['state'] == 1 and x > 15000) and (goal_score['state'] == 1 and x > goal_score['x']):
                        goal_score['state'] = 1
                        goal_score['entity_id'] = entity_id
                        goal_score['x'] = x
                    else:
                        goal_score['state'] = 1
                        goal_score['entity_id'] = entity_id
                        goal_score['x'] = x

            if (entity_type == "BLUDGER"):
                bludger.append({'entity_id': entity_id, 'entity_type': entity_type, 'x': x, 'y': y, 'vx': vx, 'vy': vy, 'state': state})
        
        # NOTE calcualte the distance between wizards and all snaffles
        k = 1
        dist_wiz0 = []
        dist_wiz1 = []
        n_snaffle = 0
        for elem in snaffle:
            x = (int)(wizard[0]['x'] + wizard[0]['vx'] * k - (elem['x'] + elem['vx'] * k))
            y = (int)(wizard[0]['y'] + wizard[0]['vy'] * k - (elem['y'] + elem['vy'] * k))
            result = x * x + y * y
            dist_wiz0.append({'wiz_snaff': result, 'snaffle_x': elem['x'], 'snaffle_y': elem['y'], 'snaffle_vx': elem['vx'], 'snaffle_vy': elem['vy'], 'snaffle_id': elem['entity_id']})
            x = (int)(wizard[1]['x'] + wizard[0]['vx'] * k - (elem['x'] + elem['vx'] * k))
            y = (int)(wizard[1]['y'] + wizard[0]['vy'] * k - (elem['y'] + elem['vy'] * k))
            result = x * x + y * y
            dist_wiz1.append({'wiz_snaff': result, 'snaffle_x': elem['x'], 'snaffle_y': elem['y'], 'snaffle_vx': elem['vx'], 'snaffle_vy': elem['vy'], 'snaffle_id': elem['entity_id']})
            n_snaffle += 1

        # NOTE: find 1st and 2nd closest snaffle to wizard0
        # NOTE: j is the count in dist_wiz
        min0_first = dist_wiz0[0]['wiz_snaff']
        min0_second = dist_wiz0[1]['wiz_snaff'] if n_snaffle > 1 else dist_wiz0[0]['wiz_snaff']
        j = 0;
        flag0_first = 0;
        flag0_second = 1 if n_snaffle > 1 else 0;
        for elem in dist_wiz0:
            if elem['wiz_snaff'] < min0_first:
                min0_second = min0_first;
                flag0_second = flag0_first
                min0_first = elem['wiz_snaff']
                flag0_first = j
            elif (elem['wiz_snaff'] < min0_second) and (elem['wiz_snaff'] > min0_first):
                min0_second = elem['wiz_snaff']
                flag0_second = j;
            j+= 1
        
        # NOTE find 1st and 2nd closest snaffle to wizard1
        min1_first = dist_wiz1[0]['wiz_snaff']
        min1_second = dist_wiz1[1]['wiz_snaff'] if n_snaffle > 1 else dist_wiz1[0]['wiz_snaff']
        j = 0;
        flag1_first = 0;
        flag1_second = 1 if n_snaffle > 1 else 0;
        for elem in dist_wiz1:
            if elem['wiz_snaff'] < min1_first:
                min1_second = min1_first;
                flag1_second = flag1_first
                min1_first = elem['wiz_snaff']
                flag1_first = j
            elif (elem['wiz_snaff'] < min1_second) and (elem['wiz_snaff'] > min1_first):
                min1_second = elem['wiz_snaff']
                flag1_second = j;
            j+= 1
    
        # NOTE make sure wizard1 and wizard0 do not hunt same ball
        flag0 = flag0_first
        flag1 = flag1_first
        if dist_wiz0[flag0_first]['snaffle_id'] == dist_wiz1[flag1_first]['snaffle_id']:
            if dist_wiz0[flag0_second]['snaffle_id'] != dist_wiz1[flag1_second]['snaffle_id']:
                if min0_first <= min1_first:
                    flag0 = flag0_first
                    flag1 = flag1_second
                else:
                    flag0 = flag0_second
                    flag1 = flag1_first
            else:
                if min0_first + min1_second < min0_second + min1_first:
                    flag0 = flag0_first
                    flag1 = flag1_second
                else:
                    flag0 = flag0_second
                    flag1 = flag1_first
      
        # NOTE: If wizard is holding a snaffle throw it to MY goal\
        
        for i in range(2):
            # Wizard has a snaffle
            if wizard[i]['state'] == 1:
                # SET WIZARD
                wiz = i

                # NOTE check if there is an obstacle in the shooting line
                clear_goal_real = []
                x2 = opponent_goal['goal_x']
                
                if wiz == 0:
                    x1, y1 = wizard[0]['x'], wizard[0]['y']
                if wiz == 1:
                    x1, y1 = wizard[1]['x'], wizard[1]['y']
                
                for elem in goal_target_points_real:
                    y2 = elem
                    count = 0
                    for i in range(2):
                        x0, y0 = opponent_wizard[i]['x'], opponent_wizard[i]['y']
                        if object_in_front_of_line(x0, y0, x1, y1, x2, y2, opponent_wizard_radius2) == 1:
                            count = 1
                            break
                        
                        x0, y0 = x0 + opponent_wizard[i]['vx'], y0 + opponent_wizard[i]['vy']
                        if object_in_front_of_line(x0, y0, x1, y1, x2, y2, opponent_wizard_radius2) == 1:
                            count = 1
                            break
                    
                    if count == 1:
                        continue
                    
                    # BLUDGER
                    for i in range (2):
                        x0, y0 = bludger[i]['x'], bludger[i]['y']
                        if object_in_front_of_line(x0, y0, x1, y1, x2, y2, bludger_radius2) == 1:
                            count = 1
                            break
    
                        x0, y0 = x0 + bludger[i]['vx'], y0 + bludger[i]['vy']
                        if object_in_front_of_line(x0, y0, x1, y1, x2, y2, bludger_radius2) == 1:
                            count = 1
                            break
    
                    if count == 1:
                        continue
                    
                    if count == 0:
                        clear_goal_real.append(elem)
                 
                snaffle_thrust = 500
                first_round = 0
                throw_x = 0
                throw_y = 0
                calc_throw_x = 0
                calc_throw_y = 0
                min_time_to_destination = 250
                if (len(clear_goal_real) > 0):
                    for elem in clear_goal_real:    
                        calc_throw_x, calc_throw_y, snaffle_v, distance_to_dest = calc_throw_vector(wizard[wiz]['x'], wizard[wiz]['y'],wizard[wiz]['vx'], wizard[wiz]['vy'], opponent_goal['goal_x'], elem, snaffle_thrust)
                        time_to_destination = distance_to_dest / snaffle_v
                        if first_round == 0:
                            min_time_to_destination = time_to_destination
                            throw_x = calc_throw_x
                            throw_y = calc_throw_y
                        else:
                            if (time_to_destination < min_time_to_destination):
                                min_time_to_destination = time_to_destination
                                throw_x = calc_throw_x
                                throw_y = calc_throw_y
                        first_round+=1
                    print ("THROW", throw_x, throw_y, snaffle_thrust)
                else:
                    clear_goal_real = []

                    if wiz == 0:
                        x1, y1 = wizard[0]['x'], wizard[0]['y']
                        x2, y2 = wizard[1]['x'] + wizard[1]['vx'], wizard[1]['y'] + wizard[1]['vy']
                    if wiz == 1:
                        x1, y1 = wizard[1]['x'], wizard[1]['y']
                        x2, y2 = wizard[0]['x'] + wizard[0]['vx'], wizard[0]['y'] + wizard[0]['vy']

                    count = 0
                    # OPPONENT 
                    for i in range(2):
                        x0, y0 = opponent_wizard[i]['x'], opponent_wizard[i]['y']
                        if object_in_front_of_line(x0, y0, x1, y1, x2, y2, opponent_wizard_radius2) == 1:
                            count = 1
                            break
                        
                        x0, y0 = x0 + opponent_wizard[i]['vx'], y0 + opponent_wizard[i]['vy']
                        if object_in_front_of_line(x0, y0, x1, y1, x2, y2, opponent_wizard_radius2) == 1:
                            count = 1
                            break
                    
                    # BLUDGER
                    for i in range (2):
                        x0, y0 = bludger[i]['x'], bludger[i]['y']
                        if object_in_front_of_line(x0, y0, x1, y1, x2, y2, bludger_radius2) == 1:
                            count = 1
                            break
    
                        x0, y0 = x0 + bludger[i]['vx'], y0 + bludger[i]['vy']
                        if object_in_front_of_line(x0, y0, x1, y1, x2, y2, bludger_radius2) == 1:
                            count = 1
                            break
                    
                    if count == 0:
                        clear_goal_real.append(elem)                     
                    
                    snaffle_thrust = 500
                    first_round = 0
                    throw_x = 0
                    throw_y = 0
                    calc_throw_x = 0
                    calc_throw_y = 0
                    min_time_to_destination = 250
                    if (len(clear_goal_real) > 0):
                        calc_throw_x, calc_throw_y, snaffle_v, distance_to_dest = calc_throw_vector(wizard[wiz]['x'], wizard[wiz]['y'],wizard[wiz]['vx'], wizard[wiz]['vy'], x2, y2, snaffle_thrust)
                        print ("THROW", throw_x, throw_y, snaffle_thrust)
                    else:
                        if wiz == 0:
                            throw_x = wizard[0]['x'] 
                            throw_y = wizard[0]['y']
                            snaffle_thrust = 0
                        if wiz == 1:
                            throw_x = wizard[1]['x']
                            throw_y = wizard[1]['y']
                            snaffle_thrust = 0
                        print ("THROW", throw_x, throw_y, snaffle_thrust)    
            else:
                # # NOTE: push snaffle into OPPONENT_GOAL
                if goal_score['state'] == 1 and my_magic > 19:
                    magic_thrust = 20
                    print ("WINGARDIUM", goal_score['entity_id'], opponent_goal['goal_x'], opponent_goal['goal_y'], magic_thrust)

                elif goal_warning['state'] == 1 and my_magic >19:  
                # saving goal warning 
                    magic_thrust = 20
                    
                    clear_goal_real = []
                    x2 = opponent_goal['goal_x']

                    for elem in snaffle:
                        if elem['entity_id'] == goal_warning['entity_id']:
                            x1 = elem['x']
                            y1 = elem['x']
                    for elem in goal_target_points_real:
                        y2 = elem
                        count = 0

                        # OPPONENT 
                        for i in range(2):
                            x0, y0 = opponent_wizard[i]['x'], opponent_wizard[i]['y']
                            if object_in_front_of_line(x0, y0, x1, y1, x2, y2, opponent_wizard_radius2) == 1:
                                count = 1
                                break
                            
                            x0, y0 = x0 + opponent_wizard[i]['vx'], y0 + opponent_wizard[i]['vy']
                            if object_in_front_of_line(x0, y0, x1, y1, x2, y2, opponent_wizard_radius2) == 1:
                                count = 1
                                break
                        
                        if count == 1:
                            continue
                        
                        # BLUDGER
                        for i in range (2):
                            x0, y0 = bludger[i]['x'], bludger[i]['y']
                            if object_in_front_of_line(x0, y0, x1, y1, x2, y2, bludger_radius2) == 1:
                                count = 1
                                break
        
                            x0, y0 = x0 + bludger[i]['vx'], y0 + bludger[i]['vy']
                            if object_in_front_of_line(x0, y0, x1, y1, x2, y2, bludger_radius2) == 1:
                                count = 1
                                break
        
                        if count == 1:
                            continue

                        if count == 0:
                            clear_goal_real.append(elem)

                    snaffle_thrust = 300
                    first_round = 0
                    throw_x = 0
                    throw_y = 0
                    calc_throw_x = 0
                    calc_throw_y = 0
                    min_time_to_destination = 250
                    if (len(clear_goal_real) > 0):
                        for elem in clear_goal_real:    
                            calc_throw_x, calc_throw_y, snaffle_v, distance_to_dest = calc_throw_vector(wizard[wiz]['x'], wizard[wiz]['y'],wizard[wiz]['vx'], wizard[wiz]['vy'], opponent_goal['goal_x'], elem, snaffle_thrust)
                            time_to_destination = distance_to_dest / snaffle_v
                            if first_round == 0:
                                min_time_to_destination = time_to_destination
                                throw_x = calc_throw_x
                                throw_y = calc_throw_y
                            else:
                                if (time_to_destination < min_time_to_destination):
                                    min_time_to_destination = time_to_destination
                                    throw_x = calc_throw_x
                                    throw_y = calc_throw_y
                            first_round+=1
                        print ("WINGARDIUM", goal_warning['entity_id'], throw_x, throw_y, magic_thrust)
                    else:
                        print ("WINGARDIUM", goal_warning['entity_id'], throw_x, throw_y, magic_thrust)

                else:
                    # NOTE: in other cases move to the closest snaffle 
                    if i == 0:
                        dist_wiz = dist_wiz0
                        flag = flag0
                    if i == 1:
                        dist_wiz = dist_wiz1
                        flag = flag1
                    (x, y) = calc_wiz_dest_coor(wizard[i]['x'], wizard[i]['y'],wizard[i]['vx'], wizard[i]['vy'], dist_wiz[flag]['snaffle_x'], dist_wiz[flag]['snaffle_y'], dist_wiz[flag]['snaffle_vx'], dist_wiz[flag]['snaffle_vy'])
                    print ("MOVE", x, y, "150")
   
if __name__ == "__main__":
    main()
