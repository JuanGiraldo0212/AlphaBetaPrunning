def is_game_over(node):
    winning_indexes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    for indexes in winning_indexes:
        hit_count = 0
        chosen_symbol = node[indexes[0]]

        for index in indexes:
            if node[index] is not None and node[index] == chosen_symbol:
                hit_count = hit_count + 1

        if hit_count == 3:
            return True, chosen_symbol

    if node.count(None) == 0:
        return True, None

    return False, None

def generate_children(node, chosen_symbol): # TODO: Create a function to generate the children states for minimax evaluation
    children=[]
    alpha=[]
    for i in range(len(node)):
        item=node[i]
        if( item is None):
            new_node=node.copy()
            new_node[i]=chosen_symbol
            children.append(new_node)
            alpha.append(evaluation_function(new_node,chosen_symbol))
    return children, max(alpha)

def generate_children_bounded(node, chosen_symbol,alpha): # TODO: Create a function to generate the children states for minimax evaluation
    children=[]
    new_alpha=alpha
    beta=0
    for i in range(len(node)):
        item=node[i]
        if( item is None):
            new_node=node.copy()
            new_node[i]=chosen_symbol
            if(evaluation_function(new_node,chosen_symbol)<=new_alpha or evaluation_function(new_node,chosen_symbol)==99999):
                beta=evaluation_function(new_node,chosen_symbol)
                children.append(new_node)
                break
            else:
                if(evaluation_function(new_node,chosen_symbol)<beta):
                    beta=evaluation_function(new_node,chosen_symbol)
                children.append(new_node)
        if(i==len(node)-1):
            new_alpha=beta


            
    return children

def evaluation_function(node,chosen_symbol):
    winning_indexes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    chosen_count=0
    counter_count=0
    for indexes in winning_indexes:
        counter=False
        for index in indexes:
            if(node[index]==alternate_symbol(chosen_symbol)):
                counter=True
        if counter:
            counter_count=counter_count+1
        else:
            chosen_count=chosen_count+1
    return chosen_count-counter_count
    #hacer la funcion



def alternate_symbol(symbol):
    return 'o' if symbol == 'x' else 'x'

def mini_max_ab(node, is_maximizing_player_turn, chosen_symbol,alpha): # TODO: Modify this minimax in order to turn it into an alpha-beta pruning version with depth cutting
    game_result = is_game_over(node)

    if game_result[0]:
        if game_result[1] is None:
            return 0, node

        return (-1, node) if is_maximizing_player_turn else (1, node)

    if is_maximizing_player_turn:
        children = generate_children(node, chosen_symbol)
    else:
        children=generate_children_bounded(node,chosen_symbol,alpha)
    children_results = list(map(
        lambda child: [
            mini_max_ab(child, not is_maximizing_player_turn, alternate_symbol(chosen_symbol),children[1])[0],
            child
        ],
        children[0]
    ))

    return max(children_results, key=str) if is_maximizing_player_turn else min(children_results, key=str)

def mini_max(node, is_maximizing_player_turn, chosen_symbol):
    game_result = is_game_over(node)

    if game_result[0]:
        if game_result[1] is None:
            return 0, node

        return (-1, node) if is_maximizing_player_turn else (1, node)

    children = generate_children(node, chosen_symbol)[0]
    children_results = list(map(
        lambda child: [
            mini_max(child, not is_maximizing_player_turn, alternate_symbol(chosen_symbol))[0],
            child
        ],
        children
    ))

    return max(children_results, key=str) if is_maximizing_player_turn else min(children_results, key=str)