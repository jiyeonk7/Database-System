import pymysql as pms
import time

host = 'localhost'
port = 3306
user = 'root'
psw = '0519'
charset = 'utf8mb4'
db = 'musicdb'

#predefine the system manager's id
sysmanager = 165411

connection = pms.connect(host, user, psw, db, port, charset = charset)


def view_mchart():
    print("--------------------------  view the chart  -------------------------------")
    print()
    print("title, genre, composer, artist, release date, album name, run time, song id")
    print()

    
    with connection.cursor() as cursor:
        #the deleted songs should not be shown in the chart
        sql = 'SELECT * FROM music'
        cursor.execute(sql)
        musicdata = cursor.fetchall()
        for row in musicdata:
            if(row[9] == None):
                #only till the song length is printed on the monitor
                print(row[:8])
            else:
                continue
            
    connection.commit()
    
    print("----------------------------------------------------------------------------")
    
    

def insert_music(mgrid):
    print()
    print("before you insert the song please check from below chart if the song already exists!")
    view_mchart()
    
    print()
    print("is the song you are trying to insert already in the chart? ")
    choice = input("[y/n]: ")
    if (choice == 'y' or choice == 'Y'):
        print()
        print("Let's continue to do other tasks")
    
    else:
        print("to insert music please fill out the form")
        print()
        
        with connection.cursor() as cursor:
            maxql = 'SELECT MAX(song_id) FROM music'
            cursor.execute(maxql)
            numdata = cursor.fetchall()
            
        connection.commit()
        
        mtitle = input("Enter the title of the song: ")
        print("--> genre: pop, ballad, dance, ost")
        mgenre = input("type its genre among the above: ")
        mcomposer = input("Enter the main composer: ")
        martist = input("Enter the main artist: ")
        mrdate = input("Enter the release date in the form of the following (ex.20191104): ")
        malbumname = input("Enter the name of the album: ")
        mruntime = input("Enter the length of the song in seconds: ")
        sid = numdata[0][0] + 1
        
        with connection.cursor() as cursor:
            sql = 'INSERT INTO music(title, genre, composer, artist, release_date, album_name, run_time, song_id, I_mgr_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (mtitle, mgenre, mcomposer, martist, mrdate, malbumname, mruntime, sid, mgrid))
        
        connection.commit()
        
        print("-------------------------------  INSERTION COMPLETE -------------------------------------")
        print("check the changed chart below")
        print()
        
        view_mchart()
    
    

def delete_music(mgrid):
    print("This is the current music chart")
    print()
    print("------------------------  view the chart  -------------------------")
    print()
    print("title, artist, release date, album name, Insert manager ID, song id")
    print()

    
    with connection.cursor() as cursor:
        #the deleted songs should not be shown in the chart
        sql = 'SELECT * FROM music'
        cursor.execute(sql)
        musicdata = cursor.fetchall()
        for row in musicdata:
            if(row[9] == None):
                print(str(row[0]) +", "+ str(row[3]) +", "+ str(row[4]) +", "+ str(row[5]) +", "+ str(row[8]) +" - id -> "+ str(row[7]))
            else:
                continue
            
            
    connection.commit()
    
    print("-------------------------------------------------------------------")
    
    deletem = input("Enter the song_id of the item you wish to delete (if you want to exit just press e): ")
    
    with connection.cursor() as cursor:
        sql = 'SELECT song_id FROM music WHERE song_id = %s'
        cursor.execute(sql, (deletem,))
        result = cursor.fetchall()
        
        if not result:
            print("That song is not currently on the chart.")
            print("please try again")
            
        else: 
            dsql = 'UPDATE music SET D_mgr_id = %s WHERE song_id = %s'
            cursor.execute(dsql, (mgrid,deletem,))
            print("This is the new music chart")
            view_mchart()
        
    connection.commit()

        
def user_tasks(ID):
    
    inputCmd = 0
    while(inputCmd != '8'):
        print()
        print("These are the menus please choose what task you wish to do.")
        print("1. Device Management")
        print("2. Playlist Management")
        print("3. Add music to your playlist")
        print("4. Delete music from your playlist")
        print("5. Get recommendations based on genres")
        print("6. Play music")
        print("7. Deactivate my account")
        print("8. Exit the system")
        inputCmd = input("Enter the number of the menu you wish to process: ")
        print()
        
        #device management
        if(inputCmd == '1'):
            print()
            print("Welcomme to device management")
            print()
            
            with connection.cursor() as cursor:
                didsql = 'SELECT device_id FROM device WHERE u_id = %s'
                cursor.execute(didsql, (ID,))
                devices = cursor.fetchall()
                
                dtypesql = 'SELECT d_type FROM device WHERE u_id = %s'
                cursor.execute(dtypesql, (ID,))
                types = cursor.fetchall()
                
                connection.commit()
                
                if not devices:
                    print("You have no registered devices.")
                    task = input("Enter 1 if you want to register new device (to exit, just press e): ")
                
                else:
                    print("HERE ARE YOUR DEVICES")
                    print()
                    for i in range(len(devices)):
                        print(str(i) + ". " + str(devices[i][0]) + " - " + str(types[i][0]))
                    
                    print()
                    task = input("Enter 1 for registration, 2 for deleting your device (to exit, just press e): ")   
                    
            #register devices
            if (task == '1'):
                print()
                print("register device")
                with connection.cursor() as cursor:
                    maxsql = 'SELECT MAX(device_id) FROM device'
                    cursor.execute(maxsql)
                    maxiresult = cursor.fetchall()
                    maxnum = maxiresult[0][0] + 1
                    
                    devicetype = input("Enter the device type (phone, tablet, pc): ")
                    
                    insertsql = 'INSERT INTO device VALUES(%s, %s, %s)'
                    cursor.execute(insertsql, (ID, maxnum, devicetype,))
                    
                connection.commit()
            
            #delete devices
            elif(task == '2'):
                print()
                print("delete device")
                print()
                did = input("Enter the id number of the device you wish to delete: ")
                
                with connection.cursor() as cursor:
                    checksql = 'SELECT device_id FROM device WHERE device_id = %s'
                    cursor.execute(checksql, (did,))
                    check = cursor.fetchall()
                    
                    if not check:
                        print("You have entered the wrong number.")
                        print("Please try again")
                    else:
                        delsql = 'DELETE FROM device WHERE device_id = %s'
                        cursor.execute(delsql, (did,))
                        print("DEVICE DELETED")
                        
                    connection.commit()
                
        #playlist management
        elif(inputCmd == '2'):
            print()
            print("Welcome to playlist management")
            print()
            
            plids = []
            
            with connection.cursor() as cursor:
                ppsql = 'SELECT playlist_id FROM playlist WHERE p_user = %s'
                cursor.execute(ppsql, (ID,))
                pid = cursor.fetchall()
                
                pnsql = 'SELECT num_song FROM playlist WHERE p_user = %s'
                cursor.execute(pnsql, (ID,))
                pns = cursor.fetchall()
                
                ptsql = 'SELECT total_time FROM playlist WHERE p_user = %s'
                cursor.execute(ptsql, (ID,))
                ptt = cursor.fetchall()
                
                if not pid:
                    print("You have no playlists.")
                    print()
                    task = input("Enter 1 create playlist, e to exit: ")
                
                else:
                    print("HERE ARE YOUR PLAYLIST(S)")
                    print()
                    print("#. playlist id -- number of songs -- total time")
                    for i in range(len(pid)):
                        plids.append(pid[i][0])
                        pt = int(ptt[i][0]/60)
                        print(str(i) +". "+ str(pid[i][0]) +" -- "+ str(pns[i][0]) + " -- about " + str(pt) + " minutes")
                        stsql = 'SELECT title FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(stsql, (pid[i][0],))
                        titles = cursor.fetchall()
                        
                        sasql = 'SELECT artist FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(sasql, (pid[i][0],))
                        artists = cursor.fetchall()
                        
                        for j in range(len(titles)):
                            print("     title: " + str(titles[j][0]) + "  (artist: " + str(artists[j][0]) + ")")
                        
                        print()
                        connection.commit()
                        
                    print()
                    task = input("Enter 1 to create playlist, 2 to delete playlists, e to exit: ")
                
            connection.commit()
            
            #create playlist
            if(task == '1'):
                print()
                with connection.cursor() as cursor:
                    maxsql = 'SELECT MAX(playlist_id) FROM playlist'
                    cursor.execute(maxsql)
                    maxiresult = cursor.fetchall()
                    maxnum = maxiresult[0][0] + 1
                    
                    cpsql = 'INSERT INTO playlist VALUES(%s, %s, %s, %s)'
                    cursor.execute(cpsql, (0, 0, maxnum, ID,))
                    
                    ppsql = 'SELECT playlist_id FROM playlist WHERE p_user = %s'
                    cursor.execute(ppsql, (ID,))
                    pid = cursor.fetchall()
                    
                    pnsql = 'SELECT num_song FROM playlist WHERE p_user = %s'
                    cursor.execute(pnsql, (ID,))
                    pns = cursor.fetchall()
                    
                    ptsql = 'SELECT total_time FROM playlist WHERE p_user = %s'
                    cursor.execute(ptsql, (ID,))
                    ptt = cursor.fetchall()
                    
                    print("HERE ARE YOUR PLAYLIST(S)")
                    print()
                    print("#. playlist id -- number of songs -- total time")
                    for i in range(len(pid)):
                        pt = int(ptt[i][0]/60)
                        print(str(i) +". "+ str(pid[i][0]) +" -- "+ str(pns[i][0]) + " -- about " + str(pt) + " minutes")
                        
                        stsql = 'SELECT title FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(stsql, (pid[i][0],))
                        titles = cursor.fetchall()
                        
                        sasql = 'SELECT artist FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(sasql, (pid[i][0],))
                        artists = cursor.fetchall()
                        
                        for j in range(len(titles)):
                            print("     title: " + str(titles[j][0]) + "  (artist: " + str(artists[j][0]) + ")")
                        
                        print()
                        connection.commit()
                        
                    print()
                    
                connection.commit()
            
            #delete playlist
            elif(task == '2'):
                print()
                #get the playlist number that the user wishes to delete
                dpid = input("Enter the id number of the playlist you wish to delete: ")
                
                with connection.cursor() as cursor:
                    plsql = 'SELECT playlist_id FROM playlist WHERE p_user = %s'
                    cursor.execute(plsql, (ID,))
                    plid = cursor.fetchall()
                    
                    for item in plid:
                        plids.append(int(item[0]))
                connection.commit()
                    
                if(int(dpid) in plids):
                    print()
                    print("------ START DELETING ----------")
                    with connection.cursor() as cursor:
                        dmpsql = 'DELETE FROM mp WHERE p_id = %s'
                        cursor.execute(dmpsql, (dpid,))
                        
                        print("> DELETING .......")
                        
                        dpsql = 'DELETE FROM playlist WHERE playlist_id = %s'
                        cursor.execute(dpsql, (dpid,))
                        
                        print()
                        print("DELETION COMPLETE")
                    
                    connection.commit()
                    
                #entered the wrong id. print warning message
                else:
                    print()
                    print("Entered the wrong number")
                    print("please try again")

        #add music to playlist
        elif(inputCmd == '3'):
            print()
            
            plids = []
            #show the playlist
            with connection.cursor() as cursor:
                ppsql = 'SELECT playlist_id FROM playlist WHERE p_user = %s'
                cursor.execute(ppsql, (ID,))
                pid = cursor.fetchall()
                
                pnsql = 'SELECT num_song FROM playlist WHERE p_user = %s'
                cursor.execute(pnsql, (ID,))
                pns = cursor.fetchall()
                
                ptsql = 'SELECT total_time FROM playlist WHERE p_user = %s'
                cursor.execute(ptsql, (ID,))
                ptt = cursor.fetchall()
                
                if not pid:
                    print("You have no playlists.")
                    print("Please go back and create the playlist first")
                    print()
                    
                else:
                    print("HERE ARE YOUR PLAYLIST(S)")
                    print()
                    print("#. playlist id -- number of songs -- total time")
                    for i in range(len(pid)):
                        pt = int(ptt[i][0]/60)
                        print(str(i) +". "+ str(pid[i][0]) +" -- "+ str(pns[i][0]) + " -- about " + str(pt) + " minutes")
                        stsql = 'SELECT title FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(stsql, (pid[i][0],))
                        titles = cursor.fetchall()
                        
                        sasql = 'SELECT artist FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(sasql, (pid[i][0],))
                        artists = cursor.fetchall()
                        
                        for j in range(len(titles)):
                            print("     title: " + str(titles[j][0]) + "  (artist: " + str(artists[j][0]) + ")")
                        
                        print()
                        connection.commit()
                        
                    print()
                    
                    #get the playlist id that he or she wants the msuic to be added
                    targetPL = input("Enter the playlist id that you wish to insert song(s) into: ")
                    
                    #check if the playlist id is valid
                    with connection.cursor() as cursor:
                        ppsql = 'SELECT playlist_id FROM playlist WHERE p_user = %s'
                        cursor.execute(ppsql, (ID,))
                        pid = cursor.fetchall()
                        
                        for item in pid:
                            plids.append(int(item[0]))
                        
                        if(int(targetPL) in plids):
                            #show them the music chart
                            view_mchart()
                            
                            #update the song numbers and total time in the playlist table
                            stqnssql = 'SELECT num_song FROM playlist WHERE playlist_id = %s'
                            cursor.execute(stqnssql, (targetPL,))
                            snumdata = cursor.fetchall()
                            snum = snumdata[0][0]
                            
                            stqstsql = 'SELECT total_time FROM playlist WHERE playlist_id = %s'
                            cursor.execute(stqstsql, (targetPL,))
                            timedata = cursor.fetchall()
                            songtime = timedata[0][0]
                            
                            songs = []
                            stqsidsql = 'SELECT s_id FROM mp WHERE p_id = %s'
                            cursor.execute(stqsidsql, (targetPL,))
                            siddata = cursor.fetchall()
                            for sid in siddata:
                                songs.append(sid[0])
                            
                            
                            #have them enter the song id that they want to add to the playlist(use while)
                            key = 0
                            while(key != 'e'):
                                print()
                                print("Make sure you do not input the same id more than once!")
                                print(songs)
                                print()
                                key = input("Enter the song id of the song that you wish to add to the playlist (insert e for exit): ")
                                                                
                                #check if the song id is valid
                                cssql = 'SELECT D_mgr_id FROM music WHERE song_id = %s'
                                cursor.execute(cssql, (key,))
                                checkmusic = cursor.fetchall()
                                
                                msql = 'SELECT MAX(song_id) FROM music'
                                cursor.execute(msql)
                                maxinum = cursor.fetchall()
                                mxn = maxinum[0][0]
                                
                                if(key == 'e'):
                                    print("Exiting the menu")
                                
                                elif(snum == 300):
                                    print("Cannot add more songs! Reached Max!")
                                 
                                else:
                                    dmgrsql = 'SELECT * FROM music WHERE song_id = %s'
                                    cursor.execute(dmgrsql, (key,))
                                    checkdmgr = cursor.fetchall()
                                   
                                    if(int(key) in songs):
                                        print("Redundant insert. Try again!")
                                        break
                                    
                                    if(int(key) > int(mxn)):
                                        print("Warning: Entered the wrong song id")
                                    
                                    elif(checkdmgr[0][9] == None):
                                        songtime = songtime + checkdmgr[0][6]
                                        songs.append(int(key))
                                        #add the pair of playlist id and song id to the mp table
                                        sisql = 'INSERT INTO mp VALUES (%s, %s)'
                                        cursor.execute(sisql, (targetPL, key,))
                                        snum = snum + 1
                                    
                                    #if the song id is invalid, ask them to try again
                                    else: 
                                        print("Warning: Entered the wrong song id")
                    
                            
                            #update the song numbers in the playlist table
                            upsnsql = 'UPDATE playlist SET num_song = %s WHERE playlist_id = %s'
                            cursor.execute(upsnsql, (snum, targetPL,))
                            
                            uptsql = 'UPDATE playlist SET total_time = %s WHERE playlist_id = %s'
                            cursor.execute(uptsql, (songtime, targetPL,))
                        
                        else:
                            print()
                            print("WARNING: ENTERED THE WRONG PLAYLIST NUMBER")
                            print()
                            break
                        
                    connection.commit()
                    
                    if(key == 'e'):
                        continue
                    
                    else:
                        #show the playlist
                        with connection.cursor() as cursor:
                            print()
                            print("HERE IS YOUR CHANGED PLAYLIST")
                            print()
                            print("#. playlist id -- number of songs -- total time")
                                  
                            snsql = 'SELECT num_song FROM playlist WHERE playlist_id = %s'
                            cursor.execute(snsql, (targetPL,))
                            sn = cursor.fetchall()
                            
                            stsql = 'SELECT total_time FROM playlist WHERE playlist_id = %s'
                            cursor.execute(stsql, (targetPL,))
                            st = cursor.fetchall()
                            totaltime = int(st[i][0]/60)
                            
                                  
                            for i in range(len(pid)):
                                pt = int(ptt[i][0]/60)
                                print(str(i) +". "+ str(pid[i][0]) +" -- "+ str(sn[i][0]) + " -- about " + str(totaltime) + " minutes")
                                stsql = 'SELECT title FROM music, mp WHERE p_id = %s AND s_id = song_id'
                                cursor.execute(stsql, (pid[i][0],))
                                titles = cursor.fetchall()
                                
                                sasql = 'SELECT artist FROM music, mp WHERE p_id = %s AND s_id = song_id'
                                cursor.execute(sasql, (pid[i][0],))
                                artists = cursor.fetchall()
                                
                                for j in range(len(titles)):
                                    print("     title: " + str(titles[j][0]) + "  (artist: " + str(artists[j][0]) + ")")
                                
                                print()
                        connection.commit()

                    
        #delete music from playlist
        elif(inputCmd == '4'):
            print()
            plids = []
            #show the playlist
            with connection.cursor() as cursor:
                ppsql = 'SELECT playlist_id FROM playlist WHERE p_user = %s'
                cursor.execute(ppsql, (ID,))
                pid = cursor.fetchall()
                
                pnsql = 'SELECT num_song FROM playlist WHERE p_user = %s'
                cursor.execute(pnsql, (ID,))
                pns = cursor.fetchall()
                
                ptsql = 'SELECT total_time FROM playlist WHERE p_user = %s'
                cursor.execute(ptsql, (ID,))
                ptt = cursor.fetchall()
                
                if not pid:
                    print("You have no playlists.")
                    print("Please go back and create the playlist first")
                    print()
                    
                else:
                    print("HERE ARE YOUR PLAYLIST(S)")
                    print()
                    print("#. playlist id -- number of songs -- total time")
                    for i in range(len(pid)):
                        plids.append(pid[i][0])
                        pt = int(ptt[i][0]/60)
                        print(str(i) +". "+ str(pid[i][0]) +" -- "+ str(pns[i][0]) + " -- about " + str(pt) + " minutes")
                        stsql = 'SELECT title FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(stsql, (pid[i][0],))
                        titles = cursor.fetchall()
                        
                        sasql = 'SELECT artist FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(sasql, (pid[i][0],))
                        artists = cursor.fetchall()
                        
                        sidsql = 'SELECT s_id FROM mp WHERE p_id = %s'
                        cursor.execute(sidsql, (pid[i][0],))
                        ids = cursor.fetchall()
                        
                        for j in range(len(titles)):
                            print("     title: " + str(titles[j][0]) + "  | artist: " + str(artists[j][0]) + "  -->  (id number: " + str(ids[j][0]) + " )")
                        
                        print()
                        connection.commit()
                        
                    print()
                    
                    #get the playlist id that he or she wants the msuic to be added
                    print("if the playlist you want to create new playlist, press b")
                    targetPL = input("Enter the playlist id that you wish to delete song(s) from: ")
                    
                    
                    
                    #check if the playlist id is valid
                    with connection.cursor() as cursor:
                        ppsql = 'SELECT playlist_id FROM playlist WHERE p_user = %s'
                        cursor.execute(ppsql, (ID,))
                        pid = cursor.fetchall()
                        
                        if(int(targetPL) in plids):
                            #update the song numbers and total time in the playlist table
                            stqnssql = 'SELECT num_song FROM playlist WHERE playlist_id = %s'
                            cursor.execute(stqnssql, (targetPL,))
                            snumdata = cursor.fetchall()
                            snum = snumdata[0][0]
                            
                            stqstsql = 'SELECT total_time FROM playlist WHERE playlist_id = %s'
                            cursor.execute(stqstsql, (targetPL,))
                            timedata = cursor.fetchall()
                            songtime = timedata[0][0]
                                                        
                            #have them enter the song id that they want to add to the playlist(use while)
                            key = 0
                            while(key != 'e'):
                                key = input("Enter the song id of the song that you wish to delete from the playlist (insert e for exit): ")
                                
                                #check if the song id is valid
                                cssql = 'SELECT D_mgr_id FROM music WHERE song_id = %s'
                                cursor.execute(cssql, (key,))
                                checkmusic = cursor.fetchall()
                                
                                if(key == 'e'):
                                    print("Exiting the menu")
                                
                                elif (checkmusic[0][0] != None):
                                    print("Entered the wrong song id")
                                    
                                else:
                                    dmgrsql = 'SELECT * FROM music WHERE song_id = %s'
                                    cursor.execute(dmgrsql, (key,))
                                    checkdmgr = cursor.fetchall()
                                    
                                    songtime = songtime - checkdmgr[0][6]
                                    
                                    if(checkdmgr[0][9] == None):
                                        #add the pair of playlist id and song id to the mp table
                                        sdsql = 'DELETE FROM mp WHERE p_id = %s AND s_id = %s'
                                        cursor.execute(sdsql, (targetPL, key,))
                                        snum = snum - 1
                                    
                                    #if the song id is invalid, ask them to try again
                                    else: 
                                        print("Entered the wrong song id")
                    
                            #update the song numbers in the playlist table
                            upsnsql = 'UPDATE playlist SET num_song = %s WHERE playlist_id = %s'
                            cursor.execute(upsnsql, (snum, targetPL,))
                            
                            uptsql = 'UPDATE playlist SET total_time = %s WHERE playlist_id = %s'
                            cursor.execute(uptsql, (songtime, targetPL,))
                        
                        else:
                            print()
                            print("WARNING: ENTERED THE WRONG PLAYLIST NUMBER")
                        
                    connection.commit()
                    
                    
        #get recommendation based on genre
        elif(inputCmd == '5'):
            print("We provide 4 genres: ost, pop, ballad, dance")
            print("Let us know which genre you want to get recommendation on and we will let you know!")
            want = input("1 for ost, 2 for pop, 3 for ballad, 4 for dance: ")
            
            if(want == '1'):
                print()
                print("you chose ost!")
                wg = 'ost'
                
            elif(want == '2'):
                print()
                print("you chose pop")
                wg = 'pop'
                
            elif(want == '3'):
                print()
                print("you chose ballad")
                wg = 'ballad'
                
            elif(want == '4'):
                print()
                print("you chose dance!")
                wg = 'dance'
            
            with connection.cursor() as cursor:
                sql = 'SELECT * FROM music WHERE genre = %s'
                cursor.execute(sql, (wg,))
                mdata = cursor.fetchall()
                
                print()
                print("GENRE: " + str(wg))
                print("---------------------------  view the chart  ------------------------------")
                print()
                print("title, genre, composer, artist, release date, album name, run time, song id")
                print()

                for data in mdata:
                    if(data[9] == None):
                        print(data[:8])
                    else:
                        continue
            
            connection.commit()
            
        
        #play music
        elif(inputCmd == '6'):
            print()
            
            plids = []
            
            with connection.cursor() as cursor:
                ppsql = 'SELECT playlist_id FROM playlist WHERE p_user = %s'
                cursor.execute(ppsql, (ID,))
                pid = cursor.fetchall()
                
                pnsql = 'SELECT num_song FROM playlist WHERE p_user = %s'
                cursor.execute(pnsql, (ID,))
                pns = cursor.fetchall()
                
                ptsql = 'SELECT total_time FROM playlist WHERE p_user = %s'
                cursor.execute(ptsql, (ID,))
                ptt = cursor.fetchall()
                
                if not pid:
                    print("You have no playlists.")
                    print("Please go and make a playlist first!")
                    print()
                    
                    
                else:
                    print("HERE ARE YOUR PLAYLIST(S)")
                    print()
                    print("#. playlist id -- number of songs -- total time")
                    for i in range(len(pid)):
                        plids.append(pid[i][0])
                        pt = int(ptt[i][0]/60)
                        print(str(i) +". "+ str(pid[i][0]) +" -- "+ str(pns[i][0]) + " -- about " + str(pt) + " minutes")
                        stsql = 'SELECT title FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(stsql, (pid[i][0],))
                        titles = cursor.fetchall()
                        
                        sasql = 'SELECT artist FROM music, mp WHERE p_id = %s AND s_id = song_id'
                        cursor.execute(sasql, (pid[i][0],))
                        artists = cursor.fetchall()
                        
                        for j in range(len(titles)):
                            print("     title: " + str(titles[j][0]) + "  (artist: " + str(artists[j][0]) + ")")
                        
                        print()
                        connection.commit()
                    
                    print()
                    pnum = input("Enter the playlist id you wish to play: ")
                    #check if the playlist id is valid
                    with connection.cursor() as cursor:
                        
                        if(int(pnum) in plids):
                            print("---------------------------------- PLAYING MUSIC ---------------------------------------")
                            stsql = 'SELECT title FROM music, mp WHERE p_id = %s AND s_id = song_id'
                            cursor.execute(stsql, (pnum,))
                            titles = cursor.fetchall()
                            
                            sasql = 'SELECT artist FROM music, mp WHERE p_id = %s AND s_id = song_id'
                            cursor.execute(sasql, (pnum,))
                            artists = cursor.fetchall()
                            
                            srtsql = 'SELECT run_time FROM music, mp WHERE p_id = %s AND s_id = song_id'
                            cursor.execute(srtsql, (pnum,))
                            runtime = cursor.fetchall()
                            
                            for j in range(len(titles)):
                                rtime = int(runtime[j][0])
                                print("PLAYING:      title: " + str(titles[j][0]) + "  (artist: " + str(artists[j][0]) + ")")
                                for t in range(rtime):
                                    time.sleep(1)
                                    
                                print()
                                terminate = input("if you want to exit press e else, press c: ")
                                
                                if(terminate == 'e'):
                                    break
                                else:
                                    continue
                            
                            print()
                            connection.commit()
                        
                            
                        else:
                            print("WARNING: ENTERED THE WRONG PLAYLIST NUMBER")
                    connection.commit()
            
            
                       
            
        
        #deactivate account
        elif(inputCmd == '7'):
            print()
            print("ARE YOU SURE THAT YOU WANT TO DEACTIVATE YOUR ACCOUNT?")
            print("by doing this, next time you want to use our syste, you will have to register all over again")
            print()
            print("Do you want to deactivate? ")
            schance = input("[y/n]: ")
            print()
            
            if(schance == 'y' or schance == 'Y'):
                print("ERASING USER INFORMATION ... ")
                print()

                with connection.cursor() as cursor:
                    ddsql = 'DELETE FROM device WHERE u_id = %s'
                    cursor.execute(ddsql, (ID,))
                    
                    pls = []
                    psql = 'SELECT playlist_id FROM playlist where p_user = %s'
                    cursor.execute(psql, (ID,))
                    pdata = cursor.fetchall()
                    for data in pdata:
                        pls.append(data[0])
                    
                    for item in pls:
                        dmpsql = 'DELETE FROM mp WHERE p_id = %s'
                        cursor.execute(dmpsql, (item,))
                    
                    dplsql = 'DELETE FROM playlist WHERE p_user = %s'
                    cursor.execute(dplsql, (ID,))
                    
                    dusql = 'DELETE FROM users WHERE u_num = %s'
                    cursor.execute(dusql, (ID,))
                    
                connection.commit()
                print("----------- DELETION COMPLETE -------------")
                print()
                print("Thank you for using our service. You are always welcome to come back to enjoy our service :)")
                break
                
                
            elif(schance == 'n' or schance == 'N'):
                print("Returning to the system")
            
            else:
                print("Please choose your answer carefully")            
            
        #exit the system        
        elif(inputCmd == '8'):
                        print("Did you do all you needed to do?")
                        print("Ready to exit the system?")
                        ans = input("[y/n]: ")
                        
                        #exit the system
                        if(ans == 'y' or ans == 'Y'):
                            print()
                            print("Good bye :)")
                            print("Have a great day!")
                            break
                        
                        #chose exit by mistake
                        elif(ans == 'n' or ans =='N'):
                            print()
                            print("Here is your second chance to pick once again :)")
                            inputCmd = 0





#beginning of the program
print()
print("===========================================")
print()
print("Welcome to THE ULTIMATE MUSIC PLATFORM")
print()
print("First, please confirm your identification")
print()

role = input("Type 1 if manager, 2 if user, 3 if you need to register: ")
print()
print("===========================================")
print()

#if manager
if (role == '1'):
    print("Hello manager :)")
    manager = input("please insert your ID number: ")
    
    #if system manager, give access to system management menus (exclusive only to the set manager id on the top)
    if manager == '165411':
        task = 0
        while(task != '3'):
            print()
            print("Welcome System Manger")
            print("1. View Data")
            print("2. Erase manager data")
            print("3. Exit system manager menu")
            task = input("Enter the number of the task: ")
            print()
            
            if(task =='1'):
                print("---------------------- View Data ---------------------")
                print("please be reminded that these data are confidential.")
                print("thus should not be publicized without permission")
                print()
                print("1. device: devices that each users have registered")
                print("2. manager: informations regarding the managers")
                print("3. music: the songs registered in the chart")
                print("4. users: information regarding the users")
                print()
                table = input("Enter the number of the table you wish to observe: ")
                
                if(table == '1'):
                    print()
                    print("------------------------  view the chart  -------------------------")
                    print()
                    print("user id, device id, device type")
                    print()
                    
                    with connection.cursor() as cursor:
                        sql = 'SELECT * FROM device'
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        for row in data:
                            print(row)
                    connection.commit()
                        
                elif(table == '2'):
                    print()
                    print("------------------------  view the chart  -------------------------")
                    print()
                    print("manager name, manager's address, manager's phone number, manager id")
                    print()
                    
                    with connection.cursor() as cursor:
                        sql = 'SELECT * FROM manager'
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        for row in data:
                            print(row)
                    connection.commit()
                
                elif(table == '3'):
                    print()
                    print("---------------------------------------  view the chart  -------------------------------------")
                    print()
                    print("title, genre, composer, artist, release date, album name, run time, song id, Insert manager ID")
                    print()
                    
                    with connection.cursor() as cursor:
                        sql = 'SELECT * FROM music'
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        for row in data:
                            print(row)
                    connection.commit()
                
                elif(table == '4'):
                    print()
                    print("-----------------------------------  view the chart  -----------------------------------------")
                    print()
                    print("user name, user id, user password, user phone number, user social security number, user number")
                    print()
                    
                    with connection.cursor() as cursor:
                        sql = 'SELECT * FROM users'
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        for row in data:
                            print(row)
                    connection.commit()
            
            #erase data of a manager
            elif(task =='2'):
                print()
                print("------------------------  view the chart  -------------------------")
                print()
                print("manager name, manager's address, manager's phone number, manager id")
                print()
                
                with connection.cursor() as curs:
                    display = 'SELECT * FROM manager'
                    curs.execute(display)
                    managertable = curs.fetchall()
                    for row in managertable:
                        print(row)
                    
                    connection.commit()
                                        
                    retired = input("Enter the manager id of the manager that you wish to erase data of (if none, just press e): ")
                    
                    checksql = 'SELECT m_id FROM manager WHERE m_id = %s'
                    curs.execute(checksql, (retired,))
                    check = curs.fetchall()
                    
                    if not check:
                        print("You have entered the wrong number")
                    else:
                        
                        insertql = 'UPDATE music SET I_mgr_id = %s WHERE I_mgr_id = %s'
                        curs.execute(insertql, (None, retired,))
                        
                        deleteql = 'UPDATE music SET D_mgr_id = %s WHERE D_mgr_id = %s'
                        curs.execute(deleteql, (None, retired,))
                        
                        sql = 'DELETE FROM manager WHERE m_id = %s'
                        curs.execute(sql, (retired, ))
                        retiredM = curs.fetchall()
                        connection.commit()
                        print("ERASE COMPLETE")
                    
                    connection.commit()
                        
                
            #return to the normal menus
            elif(task =='3'):
                print()
                print("Returning to the original menus")
                
    else:
        print("WELCOME!")           
           
    #check whether the manager's id is registered
    try: 
        with connection.cursor() as cur:
            msql = 'SELECT m_id FROM manager WHERE m_id = %s'
            cur.execute(msql, (manager,))
            result = cur.fetchall()
                        
            #he or she is not registered
            if not result:
                print()
                print("You are not registered, please try again after you register")
            
            #he or she is a manager
            else:
                print()
                print("Hi manager :) ")
                
                #provide with menus he or she can do
                print()
                
                inputCmd = 0
                while(inputCmd != '5'):
                    print()
                    print("These are the menus please choose what task you wish to do.")
                    print("1. View the music chart")
                    print("2. Insert new music")
                    print("3. Delete music")
                    print("4. Update your information")
                    print("5. Exit")
                    inputCmd = input("Enter the number of the menu you wish to process: ")
                    print()
                    
                    #task1. views the music chart
                    if(inputCmd == '1'):
                        view_mchart()
                    
                    #task2. insert new music
                    elif(inputCmd == '2'):
                        insert_music(manager)
                    
                    #task3. delete music
                    elif(inputCmd == '3'):
                        delete_music(manager)
                    
                    #task4. update information
                    elif(inputCmd == '4'):
                        print("----------------------------  view the chart  ----------------------------")
                        print()
                        print("name(1), address(2), phone number(3), id (not for update just for display)")
                        print()
                        upsql = 'SELECT * FROM manager WHERE m_id = %s'
                        cur.execute(upsql, (manager,))
                        minfo = cur.fetchall()
                        print(minfo)
                        connection.commit()
                        
                        update = input("Enter the number of the attribute you wish to change: ")
                        #change name
                        if(update == '1'):
                            cdata = input("Enter the value that you want to change to: ")
                            upd = 'UPDATE manager SET m_name = %s WHERE m_id = %s'
                            cur.execute(upd, (cdata, manager,))
                            uresult = cur.fetchall()
                            connection.commit()
                        
                        #change address
                        elif(update == '2'):
                            cdata = input("Enter the value that you want to change to: ")
                            upd = 'UPDATE manager SET m_addr = %s WHERE m_id = %s'
                            cur.execute(upd, (cdata, manager,))
                            uresult = cur.fetchall()
                            connection.commit()
                        
                        #change phone number
                        elif(update == '3'):
                            cdata = input("Enter the value that you want to change to: ")
                            upd = 'UPDATE manager SET m_contact = %s WHERE m_id = %s'
                            cur.execute(upd, (cdata, manager,))
                            uresult = cur.fetchall()
                            connection.commit()
                        
                        else:
                            print("Entered the wrong number try again please!")
                            
                    
                    #task5. exit
                    elif(inputCmd == '5'):
                        print("Did you do all you needed to do?")
                        print("Ready to exit the system?")
                        ans = input("[y/n]: ")
                        
                        #exit the system
                        if(ans == 'y' or ans == 'Y'):
                            print()
                            print("Good bye :)")
                            print("Have a great day!")
                            break
                        
                        #chose exit by mistake
                        elif(ans == 'n' or ans =='N'):
                            print()
                            print("Here is your second chance to pick once again :)")
                            inputCmd = 0
                                            
                    else:
                        print("You have entered the wrong number! Try again!")
                 
            connection.commit()
    
    finally:
        connection.close()
        
    

#if user
elif (role == '2'):
    print("Hello user :)")
    print("To confirm your identification, please log in")
    userId = input("ID: ")
    userPssw = input("Password: ")
    
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT u_num FROM users WHERE u_id = %s AND u_password = %s'
            cursor.execute(sql, (userId, userPssw,))
            result = cursor.fetchall()
            userNum = result[0][0]
            
            user_tasks(userNum)
            
        connection.commit()
    
    finally:
        connection.close()
    

#if need to register
elif (role == '3'):
    print("Hello. Let's now register!")
    registerR = input("input 1 for manager and 2 for user: ")
    
    #register as a manager
    if (registerR == '1'):
        mid = input("please enter your id number: ")
        try:
            with connection.cursor() as cursor:
                sql = 'SELECT m_id FROM manager WHERE m_id = %s'
                cursor.execute(sql, (mid,))
                result = cursor.fetchall()
                
                #he or she is new to the system
                if not result:
                    #get the other information needed and insert it
                    print("Let's register now! Shall we?")
                    mname = input("Enter your name: ")
                    maddr = input("Enter your address (only your resident city please): ")
                    mcontact = input("Enter your phone number without the hypen please: ")
                    
                    i_sql = 'INSERT INTO manager VALUES(%s, %s, %s, %s)'
                    cursor.execute(i_sql, (mname, maddr, mcontact, mid))  
                    
                    print("Welcome " + mname + " :)")
                    
                    inputCmd = 0
                    while(inputCmd != '5'):
                        print()
                        print("These are the menus please choose what task you wish to do.")
                        print("1. View the music chart")
                        print("2. Insert new music")
                        print("3. Delete music")
                        print("4. Update your information")
                        print("5. Exit")
                        inputCmd = input("Enter the number of the menu you wish to process: ")
                        print()
                        
                        #task1. views the music chart
                        if(inputCmd == '1'):
                            view_mchart()
                        
                        #task2. insert new music
                        elif(inputCmd == '2'):
                            insert_music(mid)
                        
                        #task3. delete music
                        elif(inputCmd == '3'):
                            delete_music(mid)
                        
                        #task4. update information
                        elif(inputCmd == '4'):
                            print("---------------------------  view the chart  -----------------------------")
                            print()
                            print("name(1), address(2), phone number(3), id (not for update just for display)")
                            print()
                            upsql = 'SELECT * FROM manager WHERE m_id = %s'
                            cursor.execute(upsql, (mid,))
                            minfo = cursor.fetchall()
                            print(minfo)
                            connection.commit()
                            
                            update = input("Enter the number of the attribute you wish to change: ")
                            cdata = input("Enter the value that you want to change to: ")
                            #change name
                            if(update == '1'):
                                upd = 'UPDATE manager SET m_name = %s WHERE m_id = %s'
                                cursor.execute(upd, (cdata, mid,))
                                uresult = cursor.fetchall()
                                connection.commit()
                            
                            #change address
                            elif(update == '2'):
                                upd = 'UPDATE manger SET m_addr = %s WHERE m_id = %s'
                                cursor.execute(upd, (cdata, mid,))
                                uresult = cursor.fetchall()
                                connection.commit()
                            
                            #change phone number
                            elif(update == '3'):
                                upd = 'UPDATE manager SET m_contact = %s WHERE m_id = %s'
                                cursor.execute(upd, (cdata, mid,))
                                uresult = cursor.fetchall()
                                connection.commit()
                            
                            elif(update == '4'):
                                print("WARNING: YOU MAY NOT CHANGE OR DELETE YOUR MANAGER ID NUMBER!")
                            
                            else:
                                print("Entered the wrong number try again please!")
                            
                        #task5. exit
                        elif(inputCmd == '5'):
                            print("Did you do all you needed to do?")
                            print("Ready to exit the system?")
                            ans = input("[y/n]: ")
                            
                            #exit the system
                            if(ans == 'y' or ans == 'Y'):
                                print()
                                print("Good bye :)")
                                print("Have a great day!")
                                break
                            
                            #chose exit by mistake
                            elif(ans == 'n' or ans =='N'):
                                print()
                                print("Here is your second chance to pick once again :)")
                                inputCmd = 0
                                            
                        else:
                            print("You have entered the wrong number! Try again!")
              
                #he or she is already registered
                else:
                    print("Unfortunately, you are already registered try again please :)")
                
                connection.commit()
        
        finally:
            connection.close()
    
    #register as a user
    elif (registerR == '2'):
        ussn = input("please enter your social security number: ")
        try:
            with connection.cursor() as cursor:
                sql = 'SELECT u_ssn FROM users WHERE u_ssn = %s'
                cursor.execute(sql, (ussn,))
                result = cursor.fetchall()
                
                maxsql = 'SELECT MAX(u_num) FROM users'
                cursor.execute(maxsql)
                maxnum = cursor.fetchall()
                
                check = []
                sidql = 'SELECT u_id FROM users'
                cursor.execute(sidql)
                ids = cursor.fetchall()
                for item in ids:
                    check.append(item[0])
                
                
                #he or she is new to the system
                if not result:
                    #get the other information needed and inserted it
                    print("Let's begin the register process :)")
                    uname = input("please enter your name: ")
                    
                    flag=0
                    while(flag == 0):
                        uid = input("please enter the id you want to use: ")
                        if(uid in check):
                            print("another person is using this id please try again!")
                            flag = 0
                        else:
                            flag = 1
                            
                    upssw = input("please enter the password you want to use: ")
                    ucontact = input("please enter your phone number without the hypen please: ")
                    unum = maxnum[0][0]+1 
                    
                    u_sql = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s)'
                    cursor.execute(u_sql, (uname, uid, upssw, ucontact, ussn, unum))
                    
                    print("Welcome " +uname+ " :)")
    
                    user_tasks(unum)
                
                #he or she is already registered
                else:
                    print("Unfortunately, you are already registered try again please :)")
    
                connection.commit()
        
        finally:
            connection.close()
                    
                
    
    

#if wrong input
else:
    print("wrong input. Please restart the system.")


