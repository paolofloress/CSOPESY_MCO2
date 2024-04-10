from threading import Thread, Condition

# Initialize counts and conditions
regular_count = 0
super_count = 0
team_id = 0
lock = Condition()

# This function is for regular citizens to try to form a team
def regular_citizen(rc_id):
    global regular_count, super_count, team_id
    with lock:
        print(f"Regular Citizen {rc_id} is signing up")
        regular_count += 1
        try_to_form_team()
        lock.wait()

# This function is for super citizens to try to form a team
def super_citizen(sc_id):
    global super_count, team_id
    with lock:
        print(f"Super Citizen {sc_id} is signing up")
        super_count += 1
        try_to_form_team()
        lock.wait()

# This function checks if a team can be formed and forms one if possible
def try_to_form_team():
    global regular_count, super_count, team_id
    while regular_count + super_count >= 4 and super_count > 0 and regular_count >= 2:
        team_sc = min(2, super_count)  # At most 2 Super Citizens
        team_rc = 4 - team_sc  # The rest will be Regular Citizens to make a total of 4
        regular_count -= team_rc
        super_count -= team_sc
        print(f"team {team_id} is ready and now launching to battle (sc: {team_sc} | rc: {team_rc})")
        team_id += 1
        lock.notify_all()  # Notify other threads that a team has been formed


def main():
    r = int(input("Enter the number of Regular Citizens: "))
    s = int(input("Enter the number of Super Citizens: "))
    
    # Create and start threads for Regular and Super Citizens
    for i in range(r):
        Thread(target=regular_citizen, args=(i,)).start()
    for i in range(s):
        Thread(target=super_citizen, args=(i,)).start()

if __name__ == "__main__":
    main()
