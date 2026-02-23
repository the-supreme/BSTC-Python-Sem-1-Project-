import os
import datetime

USER_FILE = "users.txt"
TRAINEE_FILE = "trainee.txt"
SPORT_PROGRAM_FILE = "sport_programs.txt"
ENROLLMENT_FILE = "enrollments.txt"
REQUEST_FILE = "requests.txt"
TRANSACTION_FILE = "transactions.txt"

def safe_open(file_name, mode="r"):
    if not os.path.exists(file_name):
        # Create the file if it doesn't exist so the code doesn't crash
        with open(file_name, "w") as f:
            pass 
    return open(file_name, mode)

def newUserSignIn(username, password, user_role):
    newUser = [username, password, user_role]
    newUserText = "|".join(newUser)
     
    with open("users.txt", "a") as file:
        file.write(newUserText)

def generate_id(filename, prefix):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    
    except FileExistsError: 
        return f"{prefix}01"
    
    max_id = 0

    for line in lines:
        data = line.strip().split("|")
        current_id_str = data[0] #assume id is always at index 0

        # remove prefix to get only the number part
        numeric_part = current_id_str[len(prefix):]
    
        if numeric_part.isdigit():
            current_num = int(numeric_part)
            if current_num > max_id:
                max_id = current_num

    # Increment and format the ID
    new_num = max_id + 1
    new_id = f"{prefix}{new_num:02d}"

    return new_id

def update_profile(file, usrnm, pswrd):
    newName = input("PLEASE ENTER NEW NAME: ")
    newUsername = input("PLEASE ENTER NEW USERNAME: ")    
    newPassword = ""
    #password verification
    while not newPassword.isalnum():
        newPassword = input("PLEASE ENTER NEW PASSWORD(A COMBINATION OF ALPHANUMERIC CHARACTERS): ")
    
        if not newPassword.isalnum():
            print("Invalid password! Please use only letters and numbers.")

    print("Password accepted.")

    with open(file, "r") as f:
        lines = f.readlines()

    #update new profile information
    for line in lines:
        data = line.strip().split("|")
        if data[1] == usrnm and data[2] == pswrd:
            data[1] = newUsername
            data[2] = newPassword
            data[3] = newName
            updatedLineText = "|".join(data)

    with open(file, "w") as f:
        for line in lines:
            if line.strip().split("|")[1] != usrnm:
                f.write(line)
            else:
                f.write(updatedLineText)
                f.write("\n")
                continue
    
    #update users.txt file
    with open("users.txt", "r") as f:
        content = f.readlines()

    for line in content:
        data = line.strip().split("|")
        if data[0] == usrnm and data[1] == pswrd:
            data[0] = newUsername
            data[1] = newPassword
            updatedUser = "|".join(data)
            print(updatedUser)

    with open("users.txt", "w") as f:
        for line in content:
            if line.strip().split("|")[0] != usrnm:
                f.write(line)
            else:
                f.write(updatedUser)
                f.write("\n")
                continue
    
def transaction_data_sync():
    #sync if month/year have changed from the occurance of last transaction
    with open("transactions.txt", "r") as file:
        content = file.readlines()

    #identify last transaction
    target_data = content[-1].strip().split("|")
    print(target_data)
    last_transaction_date = datetime.datetime.strptime(target_data[4], "%Y-%m-%d")

    current_date = datetime.datetime.now()
    print(last_transaction_date)
    print(current_date)

    #compare last transaction date with current date
    if (last_transaction_date.year, last_transaction_date.month) != (current_date.year, current_date.month):
        print("New month detected. Resetting enrollments...")

        #if new month, reset all fee/payments to default(RM0.00)
        with open("enrollments.txt", "r") as file:
            enrollment_lines = file.readlines()
        
        updated_enrollments = []

        for line in enrollment_lines:
            data = line.strip().split("|")
            data[3] = "0"
            data[4] = "Unpaid"
            new_line = "|".join(data) + "\n"
            updated_enrollments.append(new_line)

        with open("enrollments.txt", "w") as file:
            file.writelines(updated_enrollments)

        print("Data has been successfully synced with current month and year.")

def read_file_lines(filename):
    """Read all lines from a file"""
    try:
        with open(filename, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def write_file_lines(filename, lines):
    """Write lines to a file"""
    with open(filename, "w") as file:
        file.writelines(lines)

def append_to_file(filename, content):
    """Append content to a file"""
    with open(filename, "a") as file:
        file.write(content + "\n")

def find_user_by_username(filename, username):
    """Find a user in file by username"""
    lines = read_file_lines(filename)
    for line in lines:
        data = line.strip().split("|")
        if len(data) > 1 and data[1] == username:
            return data
    return None

def get_trainee_id_by_username(username):
    """Get trainee ID from username"""
    lines = read_file_lines(TRAINEE_FILE)
    for line in lines:
        data = line.strip().split("|")
        if len(data) > 1 and data[1] == username:
            return data[0]
    return None

def view_training_schedule(trainee_id):
    """View schedule of trainee's training programs"""
    print("=" * 50)
    print("VIEW TRAINING SCHEDULE")
    print("=" * 50)
    
    # Get trainee's enrolled programs
    enrollments = read_file_lines(ENROLLMENT_FILE)
    sport_programs = read_file_lines(SPORT_PROGRAM_FILE)
    
    # Find all sport IDs for this trainee
    trainee_sports = []
    for enrollment in enrollments:
        data = enrollment.strip().split("|")
        if len(data) >= 2 and data[0] == trainee_id:
            trainee_sports.append(data[1])
    
    if not trainee_sports:
        print("No enrolled programs found.")
        return
    
    # Display schedule for each sport
    print("\nYour Training Schedule:")
    print("-" * 40)
    
    found_programs = False
    for program in sport_programs:
        data = program.strip().split("|")
        if len(data) >= 6 and data[0] in trainee_sports:
            print(f"Sport: {data[1]}")
            print(f"Schedule: {data[4]}")
            print(f"Venue: {data[5]}")
            print(f"Coach: {data[2]}")
            print("-" * 40)
            found_programs = True
    
    if not found_programs:
        print("No schedule information available for enrolled programs.")

def send_change_request(trainee_id):
    """Send request to receptionist to change training program"""
    print("=" * 50)
    print("SEND CHANGE REQUEST")
    print("=" * 50)
    
    # Get trainee's current programs
    enrollments = read_file_lines(ENROLLMENT_FILE)
    current_programs = []
    
    for enrollment in enrollments:
        data = enrollment.strip().split("|")
        if len(data) >= 2 and data[0] == trainee_id:
            current_programs.append(data[1])
    
    if not current_programs:
        print("You are not enrolled in any programs.")
        return
    
    # Display current programs
    print("\nCurrent Enrollments:")
    sport_programs = read_file_lines(SPORT_PROGRAM_FILE)
    program_names = []
    
    for i, prog_id in enumerate(current_programs, 1):
        # Find program name
        prog_name = "Unknown"
        for program in sport_programs:
            data = program.strip().split("|")
            if len(data) >= 2 and data[0] == prog_id:
                prog_name = data[1]
                break
        program_names.append(prog_name)
        print(f"{i}. {prog_name} (ID: {prog_id})")
    
    # Select program to change
    try:
        choice = int(input(f"\nSelect program to change (1-{len(current_programs)}): ").strip()) - 1
        if 0 <= choice < len(current_programs):
            current_prog_id = current_programs[choice]
        else:
            print("ERROR: Invalid selection!")
            return
    except ValueError:
        print("ERROR: Please enter a valid number!")
        return
    
    # Display all available programs (excluding current one)
    print("\nAvailable Programs:")
    available_programs = []
    for program in sport_programs:
        data = program.strip().split("|")
        if len(data) >= 2 and data[0] != current_prog_id:
            available_programs.append([data[0], data[1]])
    
    if not available_programs:
        print("No other programs available.")
        return
    
    for i, prog in enumerate(available_programs, 1):
        print(f"{i}. {prog[1]} (ID: {prog[0]})")
    
    # Select new program
    try:
        new_choice = int(input(f"\nSelect new program (1-{len(available_programs)}): ").strip()) - 1
        if 0 <= new_choice < len(available_programs):
            new_prog_id = available_programs[new_choice][0]
        else:
            print("ERROR: Invalid selection!")
            return
    except ValueError:
        print("ERROR: Please enter a valid number!")
        return
    
    # Generate request ID
    request_id = generate_id(REQUEST_FILE, "REQ")
    
    # Create request record
    request_data = [request_id, trainee_id, current_prog_id, new_prog_id, "Pending"]
    request_text = "|".join(request_data)
    append_to_file(REQUEST_FILE, request_text)
    
    print(f"\n✓ Request sent successfully!")
    print(f"  Request ID: {request_id}")
    print(f"  From: {program_names[choice]} → To: {available_programs[new_choice][1]}")

def update_pending_request(trainee_id):
    """Update a pending request"""
    print("=" * 50)
    print("UPDATE PENDING REQUEST")
    print("=" * 50)
    
    # Get all pending requests for this trainee
    requests = read_file_lines(REQUEST_FILE)
    pending_requests = []
    
    for req in requests:
        data = req.strip().split("|")
        if len(data) >= 5 and data[1] == trainee_id and data[4] == "Pending":
            pending_requests.append(data)
    
    if not pending_requests:
        print("No pending requests found.")
        return
    
    # Display pending requests
    print("\nPending Requests:")
    sport_programs = read_file_lines(SPORT_PROGRAM_FILE)
    
    for i, req in enumerate(pending_requests, 1):
        # Get program names
        current_name = "Unknown"
        new_name = "Unknown"
        for program in sport_programs:
            data = program.strip().split("|")
            if len(data) >= 2:
                if data[0] == req[2]:
                    current_name = data[1]
                if data[0] == req[3]:
                    new_name = data[1]
        
        print(f"{i}. Request ID: {req[0]}")
        print(f"   From: {current_name} → To: {new_name}")
        print()
    
    # Select request to update
    try:
        choice = int(input(f"Select request to update (1-{len(pending_requests)}): ").strip()) - 1
        if 0 <= choice < len(pending_requests):
            selected_req = pending_requests[choice]
        else:
            print("ERROR: Invalid selection!")
            return
    except ValueError:
        print("ERROR: Please enter a valid number!")
        return
    
    # Display available programs for change
    print("\nAvailable Programs:")
    available_programs = []
    for program in sport_programs:
        data = program.strip().split("|")
        if len(data) >= 2 and data[0] != selected_req[2]:  # Exclude current program
            available_programs.append([data[0], data[1]])
    
    for i, prog in enumerate(available_programs, 1):
        print(f"{i}. {prog[1]} (ID: {prog[0]})")
    
    # Select new program
    try:
        new_choice = int(input(f"\nSelect new program (1-{len(available_programs)}): ").strip()) - 1
        if 0 <= new_choice < len(available_programs):
            new_prog_id = available_programs[new_choice][0]
        else:
            print("ERROR: Invalid selection!")
            return
    except ValueError:
        print("ERROR: Please enter a valid number!")
        return
    
    # Update the request
    lines = read_file_lines(REQUEST_FILE)
    updated_lines = []
    updated = False
    
    for line in lines:
        data = line.strip().split("|")
        if len(data) >= 5 and data[0] == selected_req[0]:
            data[3] = new_prog_id  # Update new program ID
            updated_line = "|".join(data)
            updated_lines.append(updated_line + "\n")
            updated = True
        else:
            updated_lines.append(line)
    
    if updated:
        write_file_lines(REQUEST_FILE, updated_lines)
        print("✓ Request updated successfully!")
    else:
        print("ERROR: Failed to update request!")

def delete_pending_request(trainee_id):
    """Delete a pending request"""
    print("=" * 50)
    print("DELETE PENDING REQUEST")
    print("=" * 50)
    
    # Get all pending requests for this trainee
    requests = read_file_lines(REQUEST_FILE)
    pending_requests = []
    
    for req in requests:
        data = req.strip().split("|")
        if len(data) >= 5 and data[1] == trainee_id and data[4] == "Pending":
            pending_requests.append(data)
    
    if not pending_requests:
        print("No pending requests found.")
        return
    
    # Display pending requests
    print("\nPending Requests:")
    sport_programs = read_file_lines(SPORT_PROGRAM_FILE)
    
    for i, req in enumerate(pending_requests, 1):
        # Get program names
        current_name = "Unknown"
        new_name = "Unknown"
        for program in sport_programs:
            data = program.strip().split("|")
            if len(data) >= 2:
                if data[0] == req[2]:
                    current_name = data[1]
                if data[0] == req[3]:
                    new_name = data[1]
        
        print(f"{i}. Request ID: {req[0]}")
        print(f"   From: {current_name} → To: {new_name}")
        print()
    
    # Select request to delete
    try:
        choice = int(input(f"Select request to delete (1-{len(pending_requests)}): ").strip()) - 1
        if 0 <= choice < len(pending_requests):
            request_id_to_delete = pending_requests[choice][0]
        else:
            print("ERROR: Invalid selection!")
            return
    except ValueError:
        print("ERROR: Please enter a valid number!")
        return
    
    # Confirm deletion
    confirm = input(f"Confirm deletion of request {request_id_to_delete}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return
    
    # Delete the request
    lines = read_file_lines(REQUEST_FILE)
    updated_lines = []
    
    for line in lines:
        data = line.strip().split("|")
        if len(data) >= 1 and data[0] != request_id_to_delete:
            updated_lines.append(line)
    
    write_file_lines(REQUEST_FILE, updated_lines)
    print("✓ Request deleted successfully!")

def view_payment_status(trainee_id):
    """View payment status and balance"""
    print("=" * 50)
    print("PAYMENT STATUS")
    print("=" * 50)
    
    # Get all enrollments for this trainee
    enrollments = read_file_lines(ENROLLMENT_FILE)
    sport_programs = read_file_lines(SPORT_PROGRAM_FILE)
    
    # Get program names
    program_names = []
    for program in sport_programs:
        data = program.strip().split("|")
        if len(data) >= 2:
            program_names.append([data[0], data[1]])
    
    # Calculate totals
    total_due = 0
    total_paid = 0
    balance_due = 0
    
    print("\nEnrollment Payment Details:")
    print("-" * 60)
    print(f"{'Program':<15} {'Total Fee':<12} {'Paid':<12} {'Balance':<12} {'Status':<10}")
    print("-" * 60)
    
    for enrollment in enrollments:
        data = enrollment.strip().split("|")
        if len(data) >= 5 and data[0] == trainee_id:
            # Find program name
            prog_name = "Unknown"
            for prog in program_names:
                if prog[0] == data[1]:
                    prog_name = prog[1]
                    break
            
            try:
                total_fee = float(data[2])
                paid = float(data[3])
            except ValueError:
                total_fee = 0.0
                paid = 0.0
            
            balance = total_fee - paid
            status = data[4] if len(data) >= 5 else "Unknown"
            
            total_due += total_fee
            total_paid += paid
            balance_due += balance
            
            print(f"{prog_name:<15} RM{total_fee:<10.2f} RM{paid:<10.2f} RM{balance:<10.2f} {status:<10}")
    
    print("-" * 60)
    print(f"\nSUMMARY:")
    print(f"Total Due:    RM{total_due:.2f}")
    print(f"Total Paid:   RM{total_paid:.2f}")
    print(f"Balance Due:  RM{balance_due:.2f}")
    
    if balance_due > 0:
        print("\n  You have outstanding balance. Please make payment at the reception.")
    else:
        print("\n All payments are settled.")

# ==================== ADMIN MENU ====================
def admin_menu(): 
    actionChoice = ""
    with open('admin.txt','r') as file:
        content = file.readlines()
    for admin in content:
        admin_data = admin.strip().split('|')
        if len(admin_data) >= 3: #safety check, program skips malformed line
            if admin_data[1] == username and admin_data[2] == password:
                print('Welcome back, ', username)
    while actionChoice != "7":
        print('='*50)
        print('1. Update Profile')
        print('2. Register New Coach')
        print('3. Delete Existing Coach')
        print('4. Register New Receptionist')
        print('5. Delete Existing Receptionist')
        print('6. View Monthly Income Report')
        print('7. Exit')
        print('='*50)
        actionChoice = input('Please select an action: ')

        if actionChoice == "1": #update profile
            print('='*50)
            print('Update Profile')
            print('='*50)
            update_profile("admin.txt", username, password)

        elif actionChoice == "2":
            print('='*50)
            print('Coach Registration Menu') #register coach
            print('='*50)
            newCoach = []
            role = 'Coach'
            coachName = input("Please enter coach's name: ")
            coachUsername = input("Please enter coach's username: ")
            coachPassword = ""
            #verify password
            while not coachPassword.isalnum():
                coachPassword = input("Please enter coach's password (alphanumeric only): ")
                
                if not coachPassword.isalnum():
                    print("Invalid password! Please use only letters and numbers.")
            
            print("Password accepted.") 

            #update new coach info    
            newCoach = [coachUsername,coachPassword,coachName]

            newCoachID = generate_id('coach.txt','C')
            newCoach.insert(0, newCoachID)
            newCoachText = '|'.join(newCoach)

            with open('coach.txt','a') as file:
               file.write(newCoachText + '\n')

            newUserSignIn(coachUsername, coachPassword, role + '\n')
            print("Registration complete!")

        elif actionChoice == "3": #delete coach
            print('='*50)
            print('Existing Coach Deletion Menu')
            print('='*50)
            coachUsername = input("Please enter coach's username: ")
            coachPassword = input("Please enter coach's password: ")
            deleteChoice = input(
                f"Please confirm action: DELETE {coachUsername}? (yes/no): "
            ).lower().strip()

            if deleteChoice == 'yes':
                found = False
                with open('coach.txt', 'r') as file:
                    lines = file.readlines()

                with open('coach.txt', 'w') as file:
                    for coach in lines:
                        data = coach.strip().split('|')
                        if data[1] == coachUsername and data[2] == coachPassword:
                            found = True
                            continue  #skip this coach (delete)
                        file.write(coach)

                if found:
                    print(f'Coach {coachUsername} has successfully been deleted.')
                else:
                    print(f'Coach {coachUsername} does not exist.')

                with open('users.txt', 'r') as file:
                    lines = file.readlines()

                #delete from users.txt
                with open('users.txt', 'w') as file:
                    for user in lines:
                        data = user.strip().split('|')
                        if data[0] == coachUsername and data[1] == coachPassword:
                            found = True
                            continue  #skip this user (delete)
                        file.write(user)

            elif deleteChoice == 'no':
                    print('Exit.')
                    break

        elif actionChoice == "4": #register receptionist
            print('='*50)
            print('Receptionist Registration Menu')
            print('='*50)
            newReceptionist = []
            role = 'receptionist'
            receptionistName = input("Please enter receptionist's name: ")
            receptionistUsername = input("Please create receptionist's username: ")
            receptionistPassword = ""

            #password verification
            while not receptionistPassword.isalnum():
                receptionistPassword = input("Please enter coach's password (alphanumeric only): ")
                
                if not receptionistPassword.isalnum():
                    print("Invalid password! Please use only letters and numbers.")

            print("Password accepted.")
            newReceptionist = [receptionistUsername, receptionistPassword,receptionistName]
            
            #generate new userID for receptionist
            newReceptionistID = generate_id('receptionist.txt', 'R')
            newReceptionist.insert(0, newReceptionistID)
            newReceptionistText = '|'.join(newReceptionist)

            #update new receptionist
            with open('receptionist.txt', 'a') as file:
                file.write(newReceptionistText + '\n')

            newUserSignIn(receptionistUsername, receptionistPassword, role + '\n')
            print("Registration complete!")

        elif actionChoice == "5": #delete receptionist
            print('='*50)
            print('Existing Receptionist Deletion Menu')
            print('='*50)
            receptionistUsername = input("Please enter receptionist's username: ")
            receptionistPassword = input("Please enter receptionist's password: ")
            deleteChoice = input(
                f"Please confirm action: DELETE {receptionistUsername}? (yes/no): "
            ).lower().strip()

            if deleteChoice == 'yes':
                found = False
                with open('receptionist.txt', 'r') as file:
                    lines = file.readlines()

                with open('receptionist.txt', 'w') as file:
                    for receptionist in lines:
                        data = receptionist.strip().split('|')
                        if data[1] == receptionistUsername and data[2] == receptionistPassword:
                            found = True
                            continue
                        file.write(receptionist)

                if found:
                    print(f'Receptionist {receptionistUsername} has successfully been deleted.')
                else:
                    print(f'Receptionist {receptionistUsername} does not exist')

                with open('users.txt', 'r') as file:
                    lines = file.readlines()

                with open('users.txt', 'w') as file:
                    for user in lines:
                        data = user.strip().split('|')
                        if data[0] == receptionistUsername and data[1] == receptionistPassword:
                                found = True
                                continue
                        file.write(user)
                        
            elif deleteChoice == 'no':
                    print('Exit.')
                    break

        elif actionChoice == "6": #monthly income
            print('='*50)
            print('View Monthly Income')
            print('='*50)
            sport_programs = []
            target_id = ''
            monthly_income = 0.0

            #display sport program options to choose from
            with open("sport_programs.txt","r") as file:
                for line in file:
                    sport_name = line.split("|")[1]
                    sport_programs.append(sport_name)

            for i in range(len(sport_programs)):
                print(f"{i+1}. {sport_programs[i]}")

            print('='*50)
            
            #take in input for sport choice and month
            try:
                sportChoice = int(input('Please enter the choice of sport: '))
                sport_input = sport_programs[sportChoice-1]
                month_input = int(input('Please enter the month (in integers): '))
                if sportChoice < 1 or sportChoice > len(sport_programs) or not (1 <= month_input <= 12):
                    raise IndexError 

                with open("sport_programs.txt", "r") as file:    
                    for line in file:
                        if line.split("|")[1] == sport_input:
                            target_id = line.split("|")[0]
                            break
                
                # find transactions happened for the sport in that month
                with open("transactions.txt", "r") as file:
                    for line in file:
                        data = line.strip().split("|")
                        if data[2] == target_id and int(data[5]) == month_input:
                            monthly_income += float(data[3])
                
                print(f'REPORT: {sport_input} (Month: {month_input})')
                print(f'Total income: RM{monthly_income:.2f}')

            except(ValueError,IndexError):
                print('Invalid input.')

        elif actionChoice == "7": #exit out of loop
            print('EXIT')
            break
        else:
            print("Invalid action choice input. Please try again. ")

# ==================== COACH MENU ====================
def coach_menu(username):
    # 1. IDENTIFY COACH
    coach_id = ""
    coach_name = ""

    if not os.path.exists("coach.txt"):
        print("Error: 'coach.txt' not found. Please run Setup Mode first.")
        return

    with open("coach.txt", "r") as file:
        for line in file:
            data = line.strip().split("|")
            if len(data) >= 4 and data[1] == username:
                coach_id = data[0]
                coach_name = data[3]
                break
    
    if coach_id == "":
        print("Login Failed: Username not found.")
        return

    while True:
        print(f"\n========== COACH PORTAL: {coach_name.upper()} ==========")
        print("1. Update Profile (Name/Password)")  
        print("2. Add Training Program")             
        print("3. Update Training Program Details")  
        print("4. Delete Training Program")          
        print("5. View Enrolled Trainees")           
        print("6. Logout")
        
        choice = input("Select action (1-6): ")

        if choice == "1":
            update_profile("coach.txt", username, password)

        elif choice == "2":
            print("\n--- ADD TRAINING PROGRAM ---")
            s_name = input("Sport Name (e.g. Tennis): ")
            s_fee = input("Fee (RM): ")
            s_sched = input("Schedule (e.g. Mon 10am), if training happens for more than one day a week(e.g. Mon 10am-12pm, Tues 5pm-6pm): ")
            s_venue = input("Venue: ")

            new_id = generate_id("sport_programs.txt", "T")
            new_line = f"{new_id}|{s_name}|{coach_id}|{s_fee}|{s_sched}|{s_venue}\n"

            with open("sport_programs.txt", "a") as file:
                file.write(new_line)
            print(f">> Success: Added {s_name} with ID {new_id}.")

        elif choice == "3":
            print("\n--- UPDATE PROGRAM ---")
            if not os.path.exists("sport_programs.txt"): 
                print("No programs file found."); continue

            with open("sport_programs.txt", "r") as file:
                all_lines = file.readlines()

            my_progs = []
            for line in all_lines:
                data = line.strip().split("|")
                if len(data) > 2 and data[2] == coach_id:
                    my_progs.append(data)
            
            if not my_progs: print("You have no programs."); continue

            # Display
            for i in range(len(my_progs)):
                print(f"{i+1}. {my_progs[i][1]} ({my_progs[i][0]})")

            try:
                sel = int(input("Select number to update: ")) - 1
                if 0 <= sel < len(my_progs):
                    target_id = my_progs[sel][0]
                    u_fee = input("New Fee: ")
                    u_sched = input("New Schedule: ")
                    u_venue = input("New Venue: ")

                    with open("sport_programs.txt", "w") as file:
                        for line in all_lines:
                            d = line.strip().split("|")
                            if d[0] == target_id:
                                file.write(f"{d[0]}|{d[1]}|{d[2]}|{u_fee}|{u_sched}|{u_venue}\n")
                            else:
                                file.write(line)
                    print(">> Update Successful.")
                else:
                    print("Invalid selection: Number out of range.")
            except ValueError: 
                print("Invalid input.")

        elif choice == "4":
            print("\n--- DELETE PROGRAM ---")
            if not os.path.exists("sport_programs.txt"): 
                continue
            with open("sport_programs.txt", "r") as file: 
                all_lines = file.readlines()
            
            #display all programs of current user(coach)
            my_progs = []
            for line in all_lines:
                d = line.strip().split("|")
                if len(d) > 2 and d[2] == coach_id: 
                    my_progs.append(d)
            
            for i in range(len(my_progs)): 
                print(f"{i+1}. {my_progs[i][1]}")
            
            try:
                sel = int(input("Select number to delete: ")) - 1
                if 0 <= sel < len(my_progs):
                    target_id = my_progs[sel][0]
                    with open("sport_programs.txt", "w") as file:
                        for line in all_lines:
                            d = line.strip().split("|")
                            if d[0] != target_id: 
                                file.write(line)
                    print(">> Deleted Successfully.")
                else:
                    print("Invalid selection: Number out of range.")
            except ValueError: 
                print("Invalid input.")
        
        elif choice == "5":
            print("\n--- ENROLLED TRAINEES ---")
         
            my_sports = []
            if os.path.exists("sport_programs.txt"):
                with open("sport_programs.txt", "r") as f:
                    for line in f:
                        d = line.strip().split("|")
                        if len(d) > 2 and d[2] == coach_id.strip(): 
                            my_sports.append(d[0])
            t_ids = []
            if os.path.exists("enrollments.txt"):
                with open("enrollments.txt", "r") as f:
                    for line in f:
                        d = line.strip().split("|")
                        if len(d) > 1 and d[1] in my_sports: 
                            t_ids.append(d[0])
            found = False

            if os.path.exists("trainee.txt"):
                with open("trainee.txt", "r") as f:
                    for line in f:
                        d = line.strip().split("|")
                        if len(d) > 3 and d[0] in t_ids:
                            print(f"- {d[3]} (ID: {d[0]})")
                            found = True
            if not found: 
                print("No trainees enrolled.")

        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid input.")

# ==================== RECEPTIONIST MENU ====================
def receptionist_menu():
    while True:
        with open("receptionist.txt", "r") as file:
            for receptionist in file:
                receptionist_data = receptionist.strip().split("|")
                if (receptionist_data[1] == username):
                    print("Welcome back ", receptionist_data[3])
                    receptionistID = receptionist_data[0]
                    receptionistName = receptionist_data[1]

        print("=" * 50)
        print("Please select an action: ")
        print("=" * 50)
        print("1. Update Profile")
        print("2. Register New Trainee and Enrol Trainee in Sport Training Program")
        print("3. Update Sport Training Programme of Trainee")
        print("4. Accept Payment from a Trainee")
        print("5. Delete Trainee who have completed Training")
        print("6. Exit")
        print("=" * 50)

        actionChoice = input("==> ")
        if actionChoice not in "1234567":
            print("Invalid input. Please try again. ")
        else:
            if actionChoice == "1":
                update_profile("receptionist.txt", username, password)
            elif actionChoice == "2":
                print("=" * 50)
                print("NEW TRAINEE REGISTRATION MENU")
                print("=" * 50)

                traineeUsername = input("Create a new trainee's USERNAME: ")
                traineePassword = ""

                while not traineePassword.isalnum():
                    traineePassword = input("Please enter trainee's password (alphanumeric only): ")
                    
                    if not traineePassword.isalnum():
                        print("Invalid password! Please use only letters and numbers.")

                print("Password accepted.")
                traineeName = input("Create a new trainee's NAME: ")
                traineePassport = input("Create a new trainee's PASSPORT NUM/IC NUM: ")
                traineeContact = input("Create a new trainee's CONTACT NUMBER: ")
                traineeAddress = input("Create a new trainee's ADDRESS: ")
                traineeEmail = input("Create a new trainee's EMAIL: ")
                newTrainee = [traineeUsername, traineePassword, traineeName, traineePassport, traineeEmail, traineeContact, traineeAddress]
                # Handle Sport Choices from File
                sport_choices = []

                with open("sport_programs.txt", "r") as file:
                    lines = file.readlines()

                for line in lines:
                    data = line.strip().split("|")
                    sport_choices.append(data[1])

                print("Sport Training Choices")
                for i in range(len(sport_choices)):
                    print(f"{i+1}. {sport_choices[i]}")

                print(f"Please enter trainee's Sport Training Programs(1 - {len(sport_choices)}): ")
                print("If multiple sport trainings are chosen, please enter in this format(eg: 1, 2, 4)")
                traineeSportChoice = list(int(i) - 1 for i in (input("==> ")).split(", "))

                # Process Selected Sports
                if (i <= len(sport_choices) for i in traineeSportChoice):
                    traineeSport = []
                    traineeSportID = []
                    traineeSportFee = []
                    with open("sport_programs.txt", "r") as file:
                        lines = file.readlines()

                    for line in lines:
                        for sport in traineeSportChoice:
                            data = line.strip().split("|")
                            if data[1] == sport_choices[sport]:
                                traineeSport.append(data[1])
                                traineeSportID.append(data[0])
                                traineeSportFee.append(data[3])
                # Generate ID and Save Trainee Data
                newTraineeID = generate_id("trainee.txt", "TR")
                newTrainee.insert(0, newTraineeID)

                newTraineeText = "|".join(newTrainee)

                with open("trainee.txt", "a") as file:
                    file.write(newTraineeText)
                    file.write("\n")

                amountPaid = "0"
                status = "Unpaid"

                for sport in range(len(traineeSportID)):
                    newEnrollmentData = [newTraineeID, traineeSportID[sport], traineeSportFee[sport], amountPaid, status]

                    with open("enrollments.txt", "a") as file:
                        newEnrollmentText = "|".join(newEnrollmentData)
                        file.write(newEnrollmentText)
                        file.write("\n")

                newUserSignIn(traineeUsername, traineePassword, "Trainee")
                
                print("Registration Complete!")

            elif actionChoice == "3":
                print("=" * 50)
                print("UPDATE TRAINEE'S SPORT TRAINING PROGRAM MENU")
                print("=" * 50)

                print("Please select and action: ")
                print("1. Delete trainee's program")
                print("2. Add trainee's new program")
                userChoice = input("==> ")

                traineeUsername = input("Enter trainee's USERNAME:  ")

                # Find Trainee ID from file
                with open("trainee.txt", "r") as file:
                    content = file.readlines()

                for line in content:
                    data = line.strip().split("|")
                    if data[1] == traineeUsername:
                        traineeID = data[0]

                if userChoice == "1":
                    # DELETE LOGIC
                    sport_choices = []
                    sport_choicesNames = []
                        
                    with open("enrollments.txt", "r") as file:
                        content = file.readlines()
                    
                    for line in content:
                        data = line.strip().split("|")
                        if data[0] == traineeID:
                            sport_choices.append(data[1])

                    with open("sport_programs.txt", "r") as file:
                        content = file.readlines()

                    for line in content:
                        for sport in sport_choices:
                            data = line.strip().split("|")
                            if data[0] == sport:
                                sport_choicesNames.append(data[1])
                    
                    print("Please choose which trainee's training program would like to delete: ")
                    print("=" * 50)
                    for i in range(len(sport_choicesNames)):
                        print(f"{i+1}. {sport_choicesNames[i]}")

                    deleteChoice = int(input("==> ")) - 1

                    # Rewrite file without the deleted record
                    with open("enrollments.txt", "r") as file:
                        content = file.readlines()
                    
                    with open("enrollments.txt", "w") as file:    
                        for line in content:
                            data = line.strip().split("|")
                            if not (data[0] == traineeID and data[1] == sport_choices[deleteChoice]):
                                file.write(line)
                            else:
                                print("skipped")
                                continue
                    print("Deletion was successful")

                elif userChoice == "2":
                    # ADD LOGIC
                    all_sports = []
                    sport_choicesNames = []
                        
                    with open("sport_programs.txt", "r") as file:
                        lines = file.readlines()

                    for line in lines:
                        data = line.strip().split("|")
                        all_sports.append(data[1])

                    print("Sport Training Choices")
                    for i in range(len(all_sports)):
                        print(f"{i+1}. {all_sports[i]}")

                    print(f"Please enter trainee's new Sport Training Program/Programs(1 - {len(all_sports)}): ")
                    print("If multiple sport trainings are chosen, please enter in this format(eg: 1, 2, 4)")
                    traineeSportChoice = list(int(i) - 1 for i in (input("==> ")).split(", "))
                    
                    if (i <= len(all_sports) for i in traineeSportChoice):
                        traineeSport = []
                        traineeSportID = []
                        with open("sport_programs.txt", "r") as file:
                            lines = file.readlines()

                        for line in lines:
                            for sport in traineeSportChoice:
                                data = line.strip().split("|")
                                if data[1] == all_sports[sport]:
                                    traineeSportID.append(data[0])
                                    traineeSport.append(data[1])

                    totalFee = "0"
                    amountPaid = "0"
                    status = "Unpaid"

                    for sport in traineeSportID:
                        newEnrollmentData = [traineeID, sport, totalFee, amountPaid, status]

                        with open("enrollments.txt", "a") as file:
                            newEnrollmentText = "|".join(newEnrollmentData)
                            file.write(newEnrollmentText)
                            file.write("\n")
                    
                    print("Record has been added.")

                else:
                    print("Invalid input. Please try again. ")

            elif actionChoice == "4":
                print("ACCEPT PAYMENT FROM TRAINEE MENU")

                traineesUnpaidPrograms = []
                traineesUnpaidProgramNames = []
                traineesUnpaidProgramFees = []
                #Which Trainee? -> Find Trainee ID
                traineeUsername = input("Please input the trainee's USERNAME: ")

                # Find Trainee ID
                try:
                    if not os.path.exists("trainee.txt"):
                        continue 
                    found = False
                    with open("trainee.txt", "r") as file:
                        trainee_datas = file.readlines()
                        
                        for trainee in trainee_datas:
                            data = trainee.strip().split("|")
                            if data[1] == traineeUsername:
                                traineeID = data[0]
                                traineeName = data[1]
                                found = True
                    if not found:
                        print("Invalid trainee's username.")
                        continue
                except ValueError:
                    print("Invalid input.")
                #What are the sport programs enrolled by this trainee?
                with open("enrollments.txt", "r") as file:
                    content = file.readlines()

                for line in content:
                    data = line.strip().split("|")
                    if data[0] == traineeID and data[4] != "Paid":
                        traineesUnpaidPrograms.append(data[1])
                        traineesUnpaidProgramFees.append(data[2])

                #Now we have a list of training IDs of sport programs that are enrolled

                with open("sport_programs.txt", "r") as file:
                    content = file.readlines()

                for line in content:
                    data = line.strip().split("|")
                    for i in range(len(traineesUnpaidPrograms)):
                        if data[0] == traineesUnpaidPrograms[i]:
                            traineesUnpaidProgramNames.append(data[1])

                #Now we have a list of the training program names

                print("Which program do you wish to pay for?")
                for i in range(len(traineesUnpaidProgramNames)):
                    print(f"{i+1}. {traineesUnpaidProgramNames[i]}")
                
                try:
                    userChoice = int(input("==>  ")) - 1
                    sportProgramPaymentChoice = traineesUnpaidPrograms[userChoice]
                    sportProgramPaymentChoiceName = traineesUnpaidProgramNames[userChoice]
                
                except:
                    TypeError("Please enter right digit.")
                print(f"Fee: {traineesUnpaidProgramFees[userChoice]}")
                print("How much you wish to pay?(e.g. 200)")
                paymentValue = float(input("==> "))
                
                with open("enrollments.txt", "r") as file:
                    content = file.readlines()

                updatedText = []

                for line in content:
                    data = line.strip().split("|")
                    if data[0] == traineeID and data[1] == sportProgramPaymentChoice:
                        print("Data Found, adding new payment... ")
                        target_data = float(data[3])
                        newPaymentValue = "{:.2f}".format(paymentValue + target_data)
                        data[3] = str(newPaymentValue)
                        remainingDue = float(data[2]) - float(newPaymentValue)
                        if float(data[3]) < float(data[2]):
                            data[4] = "Pending"
                        else:
                            data[4] = "Paid"
                    updatedText.append("|".join(data))
                        
                with open("enrollments.txt", "w") as file:
                    for line in updatedText:
                        print("Writing updated content in file... ")
                        file.write(line)
                        file.write("\n")

            #add transaction to transaction log in transactions.py
                today = datetime.date.today().strftime("%Y-%m-%d")
                now = datetime.datetime.now().strftime("%H:%M:%S")
                newTransactionID = generate_id("transactions.txt", "TX")
                
                newTransactionData = [newTransactionID, traineeID, sportProgramPaymentChoice, "{:.2f}".format(paymentValue), today]
                newTransactionDataText = "|".join(newTransactionData)

                with open("transactions.txt", "a") as file:
                    file.write(newTransactionDataText)
                    file.write("\n")

            elif actionChoice == "5":
                print("==================================================")
                print("DELETE TRAINEE WHO FINISHED TRAINING MENU")
                print("==================================================")
                deleteTraineeUsername = input("Enter trainee's USERNAME: ")

                with open("trainee.txt", "r") as file:
                    content = file.readlines()
                found = False
                for line in content:
                    data = line.strip().split("|")
                    if data[1] == deleteTraineeUsername:
                        found = True
                
                if not found:
                    print("Username not found.")
                    continue

                confirmation = input(f"Are you sure to delete trainee {deleteTraineeUsername}?: ")
                if confirmation.upper() == "YES":
                    #delete trainee from trainee.txt file
                    with open("trainee.txt", "w") as file:
                        for line in content:
                            data = line.strip().split("|")
                            if data[1] != deleteTraineeUsername:
                                file.write(line)
                            else:
                                deleteTraineeID = data[0]

                    #delete trainee from enrollment.txt
                    with open("enrollments.txt", "r") as file:
                        content = file.readlines()
                    
                    with open("enrollments.txt", "w") as file:
                        for line in content:
                            data = line.strip().split("|")
                            if data[0] != deleteTraineeID:
                                file.write(line)
                    
                    print("Deletion Successful.")
                else:
                    print("Deletion cancelled. Thank you for using our service.")
            elif actionChoice == "6":
                print("Exiting...")
                print("Thank you for visiting BSTC.")
                break
            else:
                print("Invalid input. Please try again. ")

# ==================== TRAINEE MENU ====================
def trainee_menu(username, password):
    """Main trainee menu"""
    # Get trainee ID
    trainee_id = get_trainee_id_by_username(username)
    if not trainee_id:
        print("ERROR: Trainee not found!")
        return
    
    # Get trainee info
    trainee_data = find_user_by_username(TRAINEE_FILE, username)
    if trainee_data and len(trainee_data) >= 4:
        print(f"\nWelcome back, {trainee_data[3]}!")
    
    while True:
        print("\n" + "=" * 50)
        print("TRAINEE MENU")
        print("=" * 50)
        print("1. Update Profile")
        print("2. View Training Schedule")
        print("3. Send Change Request")
        print("4. Update Pending Request")
        print("5. Delete Pending Request")
        print("6. View Payment Status")
        print("7. Exit")
        print("=" * 50)
        
        choice = input("Select option (1-7): ").strip()
        
        if choice == "1":
            update_profile("trainee.txt", username, password)
        elif choice == "2":
            view_training_schedule(trainee_id)
        elif choice == "3":
            send_change_request(trainee_id)
        elif choice == "4":
            update_pending_request(trainee_id)
        elif choice == "5":
            delete_pending_request(trainee_id)
        elif choice == "6":
            view_payment_status(trainee_id)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("ERROR: Invalid option! Please try again.")


## Main Logic
print("Welcome to Brilliant Sport Training Centre Online Management System!")
transaction_data_sync()
tryCount = 0
user_role = None

while tryCount < 3:
    username = input("Please enter your username:  ")
    password = input("Please enter your password:  ")
    found = False 

    with open("users.txt", "r") as file:
        for line in file:
            data = line.strip().split("|")
            if data[0] == username and data[1] == password:
                user_role = data[2]
                found = True
                break
    
    if found:
        break 
    else:
        tryCount += 1
        remaining = 3 - tryCount
        if remaining > 0:
            print(f"Invalid credentials. You have {remaining} attempt(s) left.\n")
        else:
            print("Too many failed attempts. Access denied.")

if user_role == "Admin":
    admin_menu()
elif user_role == "Receptionist":
    receptionist_menu()
elif user_role == "Coach":
    coach_menu(username)
elif user_role == "Trainee":
    trainee_menu(username, password)