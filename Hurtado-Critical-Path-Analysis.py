# Critical Path Analysis 

# Problem description from Williams (2013, pages 94-98)
# Williams, H. Paul. 2013. Model Building in Mathematical Programming (fifth edition). New York: Wiley. [ISBN-13: 978-1-118-44333-0]

# Python PuLP solution prepared by Thomas W. Miller
# Revised April 20, 2023
# Implemented using activities dictionary with derived start_times and end_times
# rather than time decision variables as in Williams (2013)

#from pulp import LpVariable, LpProblem, LpMaximize, LpStatus, value, LpMinimize

from pulp import *

# Create a dictionary of the activities and their durations
##FIRST LINE IS BEST CASE
activities = {'A_DescribeProduct':2, 'B_Marketing':4, 'C_Brochure':8, 'D1_Requirements':8, 'D2_SoftwareDesign':8, 'D3_SystemDesign':8, 'D4_Coding':160, 'D5_Documentation':16, 'D6_UnitTesting':20, 'D7_SystemTesting':20, 'D8_Package':12, 'E_Survey':20, 'F_Pricing':10, 'G_Implementation': 40, 'H_Proposal': 40}

##FOLLOWING LINE IS EXPECTED CASE
#activities = {'A_DescribeProduct':4, 'B_Marketing':8, 'C_Brochure':16, 'D1_Requirements':16, 'D2_SoftwareDesign':16, 'D3_SystemDesign':16, 'D4_Coding':320, 'D5_Documentation':32, 'D6_UnitTesting':40, 'D7_SystemTesting':40, 'D8_Package':24, 'E_Survey':40, 'F_Pricing':20, 'G_Implementation': 80, 'H_Proposal': 80}

##FOLLOWNG LINE IS WORST CASE
#activities = {'A_DescribeProduct':6, 'B_Marketing':12, 'C_Brochure':24, 'D1_Requirements':24, 'D2_SoftwareDesign':24, 'D3_SystemDesign':24, 'D4_Coding':480, 'D5_Documentation':48, 'D6_UnitTesting':60, 'D7_SystemTesting':60, 'D8_Package':36, 'E_Survey':60, 'F_Pricing':30, 'G_Implementation': 120, 'H_Proposal': 160}


# Create a list of the activities
activities_list = list(activities.keys())

# Create a dictionary of the activity precedences
precedences = {'A_DescribeProduct':[], 'B_Marketing':[], 'C_Brochure':['A_DescribeProduct'], 'D1_Requirements':['A_DescribeProduct'], 'D2_SoftwareDesign':['D1_Requirements'], 'D3_SystemDesign':['D1_Requirements'], 'D4_Coding':['D2_SoftwareDesign', 'D3_SystemDesign'], 'D5_Documentation':['D4_Coding'], 'D6_UnitTesting':['D4_Coding'], 'D7_SystemTesting':['D6_UnitTesting'], 'D8_Package':['D5_Documentation', 'D7_SystemTesting'], 'E_Survey':['B_Marketing', 'C_Brochure'], 'F_Pricing':['D8_Package', 'E_Survey'], 'G_Implementation': ['A_DescribeProduct', 'D8_Package'], 'H_Proposal': ['F_Pricing', 'G_Implementation']}


# Create the LP problem
prob = LpProblem("Critical Path", LpMinimize)

# Create the LP variables
start_times = {activity: LpVariable(f"start_{activity}", 0, None) for activity in activities_list}
end_times = {activity: LpVariable(f"end_{activity}", 0, None) for activity in activities_list}

# Add the constraints
for activity in activities_list:
    prob += end_times[activity] == start_times[activity] + activities[activity], f"{activity}_duration"
    for predecessor in precedences[activity]:
        prob += start_times[activity] >= end_times[predecessor], f"{activity}_predecessor_{predecessor}"

# Set the objective function
prob += lpSum([end_times[activity] for activity in activities_list]), "minimize_end_times"

# Solve the LP problem
status = prob.solve()

# Print the results
print("Critical Path time:")
for activity in activities_list:
    if value(start_times[activity]) == 0:
        print(f"{activity} starts at time 0")
    if value(end_times[activity]) == max([value(end_times[activity]) for activity in activities_list]):
        print(f"{activity} ends at {value(end_times[activity])} days in duration")

# Print solution
print("\nSolution variable values:")
for var in prob.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)

