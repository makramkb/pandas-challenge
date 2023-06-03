# Each eection should be run in a different cell


import csv
import pandas as pd

schools = pd.read_csv('schools_complete.csv')
students = pd.read_csv('students_complete.csv')
nb_of_schools = len (schools['school_name'].unique())
nb_total_students = len (students['student_name'])
total_budget = schools['budget'].sum()
avg_Math_score = students['math_score'].mean()
avg_Reading_score = students['reading_score'].mean()
students['passed_Math'] = students['math_score']>=60
nb_students_passed_Math = len (students[students['passed_Math']])
perc_students_passed_Math = round ((nb_students_passed_Math/nb_total_students)*100,2)
students['passed_Reading'] = students['reading_score']>=60
nb_students_passed_Reading = len (students[students['passed_Reading']])
perc_students_passed_Reading = round ((nb_students_passed_Reading/nb_total_students)*100,2)
perc_passed_M_R = (perc_students_passed_Math+perc_students_passed_Reading)/2

print('Total nb of all schools : ', nb_of_schools)
print('Total nb of students : ',nb_total_students)
print('Avg Math score :',avg_Math_score)
print('Avg Reading score :',avg_Reading_score)
print('Perc passing Math : ',perc_students_passed_Math)
print('Perc passing Reading : ',perc_students_passed_Reading)
print('Perc passing R and M : ',perc_passed_M_R)

#-------------------------------------------------------------------------------------------------------------------
# School Summary


ss=pd.merge(schools,students,on='school_name')
ss_1=ss.groupby(['type','school_name'])['Student ID'].count()


ss_2=ss.groupby(['type','school_name'])['budget'].max()
ss_3=pd.merge(ss_1,ss_2,on=(['type','school_name']))


ss_4=ss_3.rename(columns={'Student ID':'Total nb of students',
                                 'budget':'Total budget / school'})

ss_4['Budget / student'] = ss_4['Total budget / school']/ss_4['Total nb of students']
ss_4['Avg Math score / school']=round ( ss.groupby(['type','school_name'])['math_score'].mean(),2 )
ss_4['Avg Reading score / school']=round (ss.groupby(['type','school_name'])['reading_score'].mean(),2 )


ss['passed_Math']=ss['math_score']>=60
ss_5=ss[ss['passed_Math']]
ss_4['Students passed Math / school']=ss_5.groupby(['type','school_name'])['passed_Math'].count()
ss_4['Perc students passed Math / school'] \
= round((ss_4['Students passed Math / school']/ss_4['Total nb of students'])*100,2)


ss['passed_Reading']=ss['reading_score']>=60
ss_6=ss[ss['passed_Reading']]
ss_4['Students passed Reading / school']=ss_6.groupby(['type','school_name'])['passed_Reading'].count()
ss_4['Perc students passed Reading / school'] \
= round((ss_4['Students passed Reading / school']/ss_4['Total nb of students'])*100,2)


ss_4['Perc students passed M and R / school'] = \
(ss_4['Perc students passed Math / school'] + ss_4['Perc students passed Reading / school'])/2

# Final DF 

ss_4

#----------------------------------------------------------------------------------------------------------------
# Get the highest performing schools

import csv
import pandas as pd

schools = pd.read_csv('schools_complete.csv')
students = pd.read_csv('students_complete.csv')

top_schools = ss_4['Perc students passed M and R / school'].sort_values(ascending=False).head()
top_schools=pd.DataFrame(top_schools)
top_schools

#----------------------------------------------------------------------------------------------------------------------
# Get the lowest performing schools


bottom_schools = ss_4['Perc students passed M and R / school'].sort_values(ascending=True).head()
bottom_schools=pd.DataFrame(top_schools)
bottom_schools

#--------------------------------------------------------------------------------------------------------------
# Avg Math score per school/grade

ss_7=ss.groupby(['school_name','grade'])['math_score'].mean()
ss_7=pd.DataFrame(ss_7)
ss_7

#------------------------------------------------------------------------------------------------------------------

# Avg Reading score per school/grade

ss_8=ss.groupby(['school_name','grade'])['reading_score'].mean()
ss_8=pd.DataFrame(ss_7)
ss_8

#-----------------------------------------------------------------------------------------------------------------------
# Score school pending

spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

ss_4['Avg spending per student'] = pd.cut(ss_4['Budget / student'],
                                spending_bins,labels=labels,
                                 include_lowest=True)
ss_4

#---------------------------------------------------------------------------------------------------------------------------------
# Spending summary DataFrame

spending_summary = pd.DataFrame()
#spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Math Score"].mean()
spending_summary['Spending Math scores']=ss_4.groupby('Avg spending per student')['Avg Math score / school'].mean()
#spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_summary['Spending Reading scores']=ss_4.groupby('Avg spending per student')['Avg Reading score / school'].mean()
#spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_summary['Spending passing Math']=ss_4.groupby('Avg spending per student')['Perc students passed Math / school'].mean()
#spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
spending_summary['Spending passing Reading']=ss_4.groupby('Avg spending per student')['Perc students passed Reading / school'].mean()
#overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"])["% Overall Passing"].mean()
spending_summary['Spending passing R and M']=ss_4.groupby('Avg spending per student')['Perc students passed M and R / school'].mean()
#spending_summary['Spending Math score'] = ss_4

spending_summary
#---------------------------------------------------------------------------------------------------------------------------------------------
# size summary using cut method
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
size_summary  = pd.DataFrame()
size_summary ['School size based on performance'] = pd.cut(ss_4['Total nb of students'],
                                                          bins=size_bins,labels=labels,
                                                          include_lowest=True)
size_summary
