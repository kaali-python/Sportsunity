#!/usr/bin/env python

import sys
import os
import requests
from bs4 import BeautifulSoup
import termcolor
import hashlib
from itertools import izip
import pymongo

reload(sys)
sys.setdefaultencoding('utf-8')

class BundesligaSquads:
        
        def __init__(self,link,team):
                res = requests.get(link)
                self.soup = BeautifulSoup(res.content,"lxml")
                self.team = team
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.football_player_stats = db.football_player_stats
                
        def get_squads(self):
                table = self.soup.findAll('table',{'class':'tab-squad tab-squad-players'})

                rows=table[0].find_all('tr')
                
                print termcolor.colored(self.team.upper(),"red")
                print
                for row in rows:
                        name = row.find('td',{'class':'name'})
                        image=row.find('img')
                        self.squad=row.find_all('td')
                        try:
                            link=name.find('a')
                            self.get_football_player_stats('http://www.goal.com/'+link.get('href'))
                            print self.squad[2].text
                            if self.list_of_profile:
                                print self.squad[8].string.strip()
                                self.football_player_stats.update({'short_name':self.squad[2].text.strip(),'team_name':self.team},{'$set':{'player_image':self.player_image,'name':self.name.text.strip(),'long_name_id':\
                                        hashlib.md5(self.name.text.strip()).hexdigest(),'team_id':hashlib.md5(" ".join(self.team.split('-')).title()).hexdigest(),'team_name':self.team,'image':image.get('src'),'Jersey':\
                                        self.squad[1].string.strip(),'short_name':self.squad[2].text.strip(),'player_id':hashlib.md5(self.squad[2].text.strip()+self.squad[1].string.strip()).hexdigest(),'Nationality':\
                                        self.squad[3].find('span').get('title'),'Position':self.squad[4].string.strip(),'Age':self.squad[5].string.strip(),'Games':self.squad[6].string.strip(),'Goals':\
                                        self.squad[7].string.strip(),'Assists':self.squad[8].string.strip(),'Yellow':self.squad[9].string.strip(),'team':" ".join(self.team.split('-')).title(),'Red':\
                                        self.squad[11].string.strip(),'profile':self.list_of_profile,'other_competitions':self.list_of_other_competitions,'competition_name':'Bundesliga','sport_type':'football'}},upsert=True)
                            else:
                                self.football_player_stats.update({'short_name':self.squad[2].text.strip(),'team_name':self.team},{'$set':{'player_image':'','name':self.squad[2].text.strip(),'long_name_id':\
                                        hashlib.md5(self.squad[2].text.strip()).hexdigest(),'team_id':hashlib.md5(" ".join(self.team.split('-')).title()).hexdigest(),'team_name':self.team,'image':image.get('src'),'Jersey':\
                                        self.squad[1].string.strip(),'short_name':self.squad[2].text.strip(),'player_id':hashlib.md5(self.squad[2].text.strip()+self.squad[1].string.strip()).hexdigest(),'Nationality':\
                                        self.squad[3].find('span').get('title'),'Position':self.squad[4].string.strip(),'Age':self.squad[5].string.strip(),'Games':self.squad[6].string.strip(),'Goals':\
                                        self.squad[7].string.strip(),'Assists':self.squad[8].string.strip(),'Yellow':self.squad[9].string.strip(),'team':" ".join(self.team.split('-')).title(),'Red':\
                                        self.squad[11].string.strip(),'profile':self.list_of_profile,'other_competitions':self.list_of_other_competitions,'competition_name':'Bundesliga','sport_type':'football'}},upsert=True)

                        except Exception,e:
                            pass
                            
                manager = self.soup.find('table',{'class':'tab-squad tab-squad-manager'})
                manager_name = manager.find_all('td')
                self.image = manager_name[0].find('img')
                print 
                #print image.get('src') 
                print manager_name[1].text

                """
                for name in table[0].findAll('td',{'class':'name'}):
                    link=name.find('a')
                    self.get_football_player_stats('http://www.goal.com/'+link.get('href'))
                    print
                """

        def get_football_player_stats(self,link):
                res = requests.get(link)
                soup = BeautifulSoup(res.content)
                self.list_of_other_competitions = []
                self.list_of_profile = []
                try:
                    self.name=soup.findAll('div',{'id':'playerStatsCard'})[0].find('td',{'class':'playerName'})

                    stat_table = soup.findAll('div',{'class':'playerGameStatsContainer'})

                    image = soup.findAll('td',{'class':'playerPicture'})[0].find('img').get('src')

                    if not 'dummy' in image:
                            self.player_image = image
                    else:
                            pass

                    print
                    try:
                        self.list_of_profile.append({soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[0].text:soup.findAll('div',{'id':\
                                                    'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[1].text,soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[1].text:\
                                                    soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[2].text,soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':\
                                                    'playerStatLabel'})[2].text:soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[3].text,\
                                                    soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[3].text:soup.findAll('div',{'id':\
                                                        'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[4].text})
                    
                    except Exception,e:
                        self.list_of_profile.append({soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[0].text:soup.findAll('div',{'id':\
                                                'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[1].text,soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[1].text:\
                                                soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[2].text,soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':\
                                                'playerStatLabel'})[2].text:soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[3].text})

                    for stat in stat_table[0].findAll('tr'):
                        column = stat.findAll('td')
                        try:
                            self.list_of_other_competitions.append({'league':column[0].text,'team':column[1].text,'games':column[2].text,'goals':column[3].text,'assists':column[4].text,'yellow_card':\
                                    column[5].text,'red_card':column[6].text})
                        except:
                            pass

                except Exception,e:
                    pass

                return

                """
                for player in self.football_player_stats.find():
                    self.football_player_stats.update({'short_name':player['short_name']},{'$set':{'name':name.text.strip(),'profile':list_of_profile,'other_competitions':list_of_other_competitions}})
                """            
    

def main():
        list_of_teams = ['augsburg','bayer-leverkusen','bayern-munchen','borussia-dortmund','borussia-mgladbach',\
                'darmstadt-98','eintracht-frankfurt','hamburger-sv','hannover-96','hertha-bsc','hoffenheim',\
                'ingolstadt','koln','mainz-05','hoffenheim','schalke-04','stuttgart','werder-bremen','wolfsburg']

        list_of_ids = ['/1000?ICID=TP_TN_90','/963?ICID=TP_TN_91','/961?ICID=TP_TN_99','/964?ICID=SP_TN_93',\
                '/971?ICID=TP_TN_94','/2549?ICID=TP_TN_95','/979?ICID=TP_TN_103','/967?ICID=TP_TN_104',\
                '/972?ICID=TP_TN_98','/974?ICID=TP_TN_99','/1001?ICID=TP_TN_119','/5476?ICID=TP_TN_120','/980?ICID=TP_TN_121',\
                '/977?ICID=TP_TN_122','/1001?ICID=TP_TN_119','/966?ICID=TP_TN_123','/962?ICID=TP_TN_124','/960?ICID=TP_TN_125',\
                '/968?ICID=TP_TN_126']

        for team,_id in izip(list_of_teams,list_of_ids):
            url = 'http://www.goal.com/en-us/teams/germany/bundesliga/9/'+team+_id
            obj = BundesligaSquads(url,team)
            obj.get_squads()


if __name__=='__main__':main()
