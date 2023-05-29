import pandas as pd


schools=pd.read_csv('schools_complete.csv')
students=pd.read_csv('students_complete.csv')

Total_nb_schools = len ( schools['school_name'].unique() )
print('Total nb of schools is : ',Total_nb_schools)

Total_nb_students = len (students['student_name'])
print('Total nb of students in all schools is : ',Total_nb_students)

Total_budget_for_all_schools = schools['budget'].sum()
print('The total budget of all schools is : ',Total_budget_for_all_schools )

Avg_Math_score = round (students['math_score'].mean() , 2)
print('The avg Math score for all schools is : ', Avg_Math_score)

Avg_Reading_score = round (students['reading_score'].mean() , 2)
print('The avg Reading score for all schools is : ', Avg_Reading_score)

Math_students_passed=len (students[students['math_score']>=60])
perc_passed_Math_all_schools = round ((Math_students_passed / Total_nb_students)*100,2)
print('Total percentage who passed Math in all schools is : ',perc_passed_Math_all_schools,'%' )


Reading_students_passed=len (students[students['reading_score']>=60])
perc_passed_Reading_all_schools = round ((Reading_students_passed / Total_nb_students)*100,2)
print('Total percentage who passed Reading in all schools is : ',perc_passed_Reading_all_schools,'%' )

perc_passed_Math_and_Reading_all_schools = (perc_passed_Math_all_schools+perc_passed_Reading_all_schools)/2
print('Total percentage who passed Reading and Math in all schools is : ',perc_passed_Math_and_Reading_all_schools,'%' )

#--------------------------------------------------------------------------------

# count total students and get the budget sum for each school 

total_students = students.groupby('school_name')['student_name'].count()
total_budget= schools.groupby('school_name')['budget'].sum()

# merge the result to get a DataFrame with the result
df=pd.merge(total_students,total_budget,on='school_name')

#rename the columns to reflect the purpose of each column
df=df.rename(columns={'student_name':'Total student',
                     'budget':'per school budget'})

#calculate the budget/student and add the column to df
df['per student budget']=df['per school budget']/df['Total student']
df['Avg_Math_score_per_school'] = round(students.groupby('school_name')['math_score'].mean(),2)

#calculate the avg reading score/school and add the column to df
df['Avg_Reading_score_per_school']=round (students.groupby('school_name')['reading_score'].mean(),2)


#calculate the nb of students who got 60 plus in Math per school, get the percentage and add the column to df

nb_passed_Math = students[students['math_score']>=60]
df['nb_passed_Math']=nb_passed_Math.groupby('school_name')['math_score'].count()
df['perc_passed_Math'] = round((df['nb_passed_Math']/df['Total student'])*100,2)


#calculate the nb of students who got 60 plus in Reading per school, get the percentage and add the column to df


nb_passed_reading = students[students['reading_score']>=60]
df['nb_passed_reading']=nb_passed_reading.groupby('school_name')['reading_score'].count()
df['perc_passed_reading'] = round((df['nb_passed_reading']/df['Total student'])*100,2)

#calculate the perc for students passed M and R per school and add the column to df 


df['perc_passed_M_and_R']=(df['perc_passed_Math']+df['perc_passed_reading'])/2

# df is the final result

df

#-------------------------------------------------------------------------------------------
# create a DataFrame with school_name and perc_passed_M_and_R columns and get the top 5/ bottom 5
df_1=df.reset_index()
top_schools=df_1[['school_name','perc_passed_M_and_R']].sort_values('perc_passed_M_and_R',ascending=False).head()
top_schools

bottom_schools=df_1[['school_name','perc_passed_M_and_R']].sort_values('perc_passed_M_and_R',ascending=False).tail()
bottom_schools

#-------------------------------------------------------------------------------------------------------
#create spending range column

spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]
df['Avg spending range']=pd.cut(df['per student budget'],
                              spending_bins,labels=labels,
                               include_lowest=True)
df
#------------------------------------------------------------------------------------------------------------------
# spending summary table grouping by Avg spending range

spending_summary=pd.DataFrame()
spending_summary['Avg Math score'] = df.groupby(["Avg spending range"])["Avg_Math_score_per_school"].mean()
spending_summary['Avg Reading score'] = df.groupby(["Avg spending range"])["Avg_Reading_score_per_school"].mean()
spending_summary['Avg perc passing Math'] = df.groupby(["Avg spending range"])["perc_passed_Math"].mean()
spending_summary['Avg spending passing Reading'] = df.groupby(["Avg spending range"])["perc_passed_reading"].mean()
spending_summary['Avg passing M and R'] = df.groupby(["Avg spending range"])["perc_passed_M_and_R"].mean()
spending_summary

#------------------------------------------------------------------------------------------------------
# group schools by size

size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
size_summary=pd.DataFrame()
size_summary['per school summary']=pd.cut(df['Total student'],
                                   size_bins,labels=labels,
                                   include_lowest=True)
size_summary
