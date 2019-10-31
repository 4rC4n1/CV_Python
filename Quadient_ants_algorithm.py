# User inputs for green/blue ant colony and number of steps
green_ants_count = int(input("Number of Green ants: "))
blue_ants_count = int(input("Number of Blue ants: "))
number_of_turns = int(input("Number of steps: "))

ant_color_dict = {"green" : "X",
                  "blue"  : "O"}

ant_line_lst = []
# Fill list with ants
for i in range(green_ants_count): ant_line_lst.append(ant_color_dict["green"])
for i in range(blue_ants_count): ant_line_lst.append(ant_color_dict["blue"])
print(ant_line_lst)

# Loop by number of steps from input
while number_of_turns > 0: 
    skip_move = False               # Check for double moves          
              
    # Iterates through list of ants and check neighboring enemy ants                
    for ant in range(0,len(ant_line_lst)-1):

        # Switch of two enemy neighbor ants
        if ant_line_lst[ant] != ant_line_lst[ant+1] and ant_line_lst[ant]==ant_color_dict["green"] and skip_move == False :
            ant_line_lst[ant] = ant_color_dict["blue"]
            ant_line_lst[ant+1] = ant_color_dict["green"]
            skip_move = True
  
        else:
            skip_move = False
    
    number_of_turns -= 1
    print(ant_line_lst)
