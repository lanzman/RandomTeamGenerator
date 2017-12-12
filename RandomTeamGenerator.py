#change current working directory
import os

#set folderlocation for files
folderloc = "C:\\Users\\mike.lanza\\Downloads"

#change location for saved files
os.chdir(folderloc)

import pandas as pd

#read in csv
people = pd.read_csv('Birthday Party Scavenger Hunt Bar Crawl - People.csv')

#sort out confirmed people
confirmed_list = pd.DataFrame(people[people.Status == 'Confirmed'])

#create the Team # column
confirmed_list.loc[:,'TeamNum'] = 0

#find total num people
num_people = len(confirmed_list)

#find total num guys
num_guys = len(confirmed_list.loc[confirmed_list.Sex == 'M'])

#find total num girls
num_girls = len(confirmed_list.loc[confirmed_list.Sex == 'F'])

print('# People = ', num_people)

print('# Guys = ', num_guys)

print('# Girls = ', num_girls)

from random import *

#sets size of teams
teamsize = 5

#set up num of teams to 4
teams = range(1,5)

#loop through creation of teams
for i in teams:
    
    if i != teams[-1]:
        
        #find all the female members
        femalemembers = confirmed_list.loc[(confirmed_list.Sex == 'F') & (confirmed_list['TeamNum'] == 0)]
        
        #randomly sample 2 females from pool and set the TeamNum
        confirmed_list.loc[femalemembers.sample(2).index, 'TeamNum'] = i
        
        #find the couplenum from the females chosen for the group
        couplenum = confirmed_list.loc[confirmed_list['TeamNum'] == i, 'CoupleNum'].values
        
        #find all the members who are Male, not on a team, and have either no CoupleNum or a CoupleNum not equal to the current female
        malemembers = confirmed_list[(confirmed_list.Sex == 'M') & (confirmed_list['TeamNum'] == 0) & ((confirmed_list['CoupleNum'] != confirmed_list['CoupleNum']) | (~confirmed_list['CoupleNum'].isin(couplenum)))]    
        
        #randomly sample 3 males from pool and set the TeamNum
        confirmed_list.loc[malemembers.sample(3).index, 'TeamNum'] = i
        
    #create a list of who is left
    remainingmembers = confirmed_list.loc[(confirmed_list['TeamNum'] == 0)]
    
    if i == teams[-1]:
        
        confirmed_list.loc[(confirmed_list['TeamNum'] == 0),['TeamNum']] = i
        
    #find the number of remainingmembers
    numremaining = len(remainingmembers)
    
    #find the current team members
    teammembers = confirmed_list.loc[(confirmed_list['TeamNum'] == i)]
    
    #find the number of members
    nummembers = len(teammembers)
    
#    #loop through all of the remainingmembers and randomly order them so they can be looped through
#    for member in confirmed_list.loc[(confirmed_list['TeamNum'] == 0) & (confirmed_list['Sex'] == 'M')].sample(numremaining).itertuples():
#        
#        #if there are only limited members remaining 
#        if (numremaining <= (teamsize - nummembers)):
#            
#            pass
#        
#        #if a member is not a couple or does not have a partner on the team
#        elif ((member.CoupleNum != member.CoupleNum) or (0 == sum(teammembers.CoupleNum.isin([member.CoupleNum])))):
#            
#            pass
#        
#        else:
#            
#            continue
#        
#        #adds the member to the team
#        confirmed_list.loc[member.Index, 'TeamNum'] = i
#        
#        #update the teammembers                
#        teammembers = confirmed_list.loc[(confirmed_list['TeamNum'] == i)]
#        
#        #update the number of people on the team
#        nummembers = len(teammembers)
#        
#        #if the team has 5 people, move onto the next team
#        if nummembers < 5:
#            
#            continue
#        
#        else:
#            
#            break

#sort the list by the TeamNum
confirmed_list = confirmed_list.sort_values(by = 'TeamNum', axis = 0)

team = 1
print(confirmed_list[confirmed_list.TeamNum == team])

team = 2
print(confirmed_list[confirmed_list.TeamNum == team])

team = 3
print(confirmed_list[confirmed_list.TeamNum == team])

team = 4
print(confirmed_list[confirmed_list.TeamNum == team])

confirmed_list.to_csv('TeamList.csv')

###Current state works unless it picks 2 females for each of the first teams.  This results in 0 females to sample from.
###Future update should be modified pending num of people.  If staying at 6, sample 2 females and leave last team 4 guys.

###Once final count is determined, think about switching number of members on the team so that only one team has more people
###ie: switch to teams of 3 teams of 4 and one team of 5
###also think how to get the team with extra people to have more girls
