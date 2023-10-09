import pandas as pd
pip install pulp
import pulp
df=pd.read_csv("TeacherPreferences.csv")
df.column
df.shape[1]
def calculate_updated_preference(row):
    years_of_experience = row['YrOfExp']
    rank = row['Rank']
    if rank == 'Assoc':
        increase_value = 0.4
    elif rank in ['Assistant', 'Lecturer']:
        increase_value = 0.2
    elif rank == 'Prof':
        increase_value = 0.6

    for col in df.columns[3:]:
        row[col] = row[col] + 0.001 * years_of_experience + increase_value

    return row

# Apply the function to each row
df = df.apply(calculate_updated_preference, axis=1)
df.head(15)
prob = pulp.LpProblem("Professor_Class_Assignment", pulp.LpMaximize)

# Define decision variables
num_faculty = len(df)
num_courses = len(df.columns) - 3  # Exclude the first 3 columns (ProfName, YrOfExp, Rank)

# Create a binary variable for each combination of professor and course
x = pulp.LpVariable.dicts("prof_course", ((i, j) for i in range(num_faculty) for j in range(num_courses)), cat='Binary')

# Define the objective function (maximize the sum of preferences)
objective = pulp.lpSum(df.iloc[i, j+3] * x[(i, j)] for i in range(num_faculty) for j in range(num_courses))
prob += objective

# Define constraints
for i in range(num_faculty):
    if df.iloc[i, 2] in ['Lecturer', 'Assistant']:
        prob += pulp.lpSum(x[(i, j)] for j in range(num_courses)) <= 3
    elif df.iloc[i, 2] == 'Assoc':
        prob += pulp.lpSum(x[(i, j)] for j in range(num_courses)) <= 4
    elif df.iloc[i, 2] == 'Prof':
        prob += pulp.lpSum(x[(i, j)] for j in range(num_courses)) <= 5
        
for j in range(num_courses):
    prob += pulp.lpSum(x[(i, j)] for i in range(num_faculty)) == 1
    
# Solve the problem
prob.solve()

# Extract the solution
solution = [[pulp.value(x[(i, j)]) for j in range(num_courses)] for i in range(num_faculty)]

# Print the results
for i in range(num_faculty):
    for j in range(num_courses):
        if solution[i][j] == 1:
            print(f"Professor {df.iloc[i, 0]} assigned to Course {df.columns[j+3]}")



