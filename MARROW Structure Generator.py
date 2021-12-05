#import library
import numpy as np
import matplotlib.pyplot as plt
from math import *
import csv
#read csv function
def read_csv(path):
    rows = []
    with open(path) as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            rows.append(list(row))
    return rows
#Main function
def MARROW_STRUCTURE_GENERATOR():
    excelorderdata=read_csv(Excelfilename)#extract excel data
    #calculate total number of block
    total_number_of_block=0
    for i in excelorderdata[1][2::]:
        if i=='':
            break
        total_number_of_block+=1
    #

    #Setting the Layout: Rows and Columns
    total_number_of_blocks=total_number_of_block
    layout_number_of_rows=1
    layout_number_of_columns=1
    layout_satisfied=False
    for i in range(100):#Using loop to increase i and k to fulfill total number of blocks
        if layout_satisfied:
            break
        for k in range(i+1):
            if layout_satisfied:
                break
            if i*k>=total_number_of_blocks:
                layout_number_of_rows=i
                layout_number_of_columns=k
                layout_satisfied=True
    #

    
    f1 = plt.figure("MARROW_STRUCTURES")#setup the figure and name as "MARROW_STRUCTURES"

    #setup the initial variables
    current_block_index=-1 #the block index which currently generate
    lstofinputtype=[]
    lstofleft=[]
    lstofright=[]
    lstofrow=[]
    lstofrepeat=[]
    lstoftype=[]
    lstoftwist=[]
    lstoffacet=[]
    lstofangle=[]
    lstofforallopacity=[]#for <All> mode: list of Opacity for <All> mode.
    lstofsptrans=[]#for <Specific> mode: list of Transparency crease index for <Specific> mode
    lstofspopaci=[]#for <Specific> mode: list of Opacity crease index and opacity level (in x %) for <Specific> mode

    lst_of_all=[lstofinputtype,lstofleft,lstofright,lstofrow,lstofrepeat,lstoftype,lstoftwist,lstoffacet,lstofforallopacity]#lst which include all the information lsts
    #

    ##Key in the data into each lst mentioned above

    #Each general row in the excel sheet
    current_exceldata_row_index=2
    for current_list in lst_of_all:
        for j in excelorderdata[current_exceldata_row_index][2::]:
            current_list.append(j)
        current_exceldata_row_index+=1
    #

    #Special row for <Specific> mode: Opacity and transparency data
    for jj in range(len(excelorderdata[11])):
        decider_is_transparency=False
        for j in excelorderdata[11::]:
            if j[jj]=='Opacity':
                decider_is_transparency=False       
            if j[jj]!=''and decider_is_transparency:
                lstofsptrans.append(j[jj])
            if j[jj]=='Transparency':
                decider_is_transparency=True
        decider_is_opacity=False
        for j in excelorderdata:  
            if j[jj]!=''and decider_is_opacity:
                lstofspopaci.append(j[jj])
            if j[jj]=='Opacity':
                decider_is_opacity=True 
    print(lstofspopaci)
    print(lstofsptrans)
    #

    #Special row for <facet> function: Angle of facet
    for jj in lstoffacet:
        if jj!='0':
            lstofangle.append('Facet')
        else:
            lstofangle.append(jj)
    #

    ##

    
    ##Process each block
    for ll in range(total_number_of_block):
        #retrieve current block parameters
        current_block_index+=1
        choice_ratio_or_angle=lstofinputtype.pop(0)
        current_block_choice_ratio_or_angle=lstoftype.pop(0)
        current_block_total_number_of_row=lstofrow.pop(0)
        current_block_total_number_of_column=lstofrepeat.pop(0)
        twist=lstoftwist.pop(0)#Twist option for current block
        facet=lstofangle.pop(0)#Facet angle option for current block
        #

        #If choice is angle <A>, convert to ratio (before converting to ratio, convert degree to radian, python using radian)
        if choice_ratio_or_angle=='A':
            angle_left_part=lstofleft.pop(0)
            ratio_left_part=str(sin(float(angle_left_part)/180*pi))+'/'+str(sin((90-float(angle_left_part))/180*pi))#converting degree to radian, radian to ratio
            angle_right_part=lstofright.pop(0)
            ratio_right_part=str(sin(float(angle_right_part)/180*pi))+'/'+str(sin((90-float(angle_right_part))/180*pi))
        #

        #If choice is ratio <R>, convert to float
        if choice_ratio_or_angle=='R':
            ratio_left=lstofleft.pop(0)
            ratio_right=lstofright.pop(0)
            ratio_left_part=str(float(ratio_left.split('/')[0])/5)+'/' +str(float(ratio_left.split('/')[1])/5)
            ratio_right_part=str(float(ratio_right.split('/')[0])/5)+'/' +str(float(ratio_right.split('/')[1])/5)
        #
        
        #Retrieve facet angle data
        if facet=='Facet':
            anglefacet=lstoffacet.pop(0)#facet angle in degree
            facet_angle=float(float(anglefacet)/180*pi)#facet angle in radian
        #

        #if user input <Twist>, set need_twist to True and block can twist.
        if twist=='Twist':
            need_twist=True
        else:
            need_twist=False
        #

        ##Processing ratio
        #extract demoninator and numerator
        lst=ratio_left_part.split('/')
        lst2=ratio_right_part.split('/')
        #

        #converting left and right ratio by cross multiplication
        raw_data_of_a=float(lst[0])*float(lst2[0])
        raw_data_of_b=float(lst[1])*float(lst2[0])
        raw_data_of_c=float(lst[0])*float(lst2[0])
        raw_data_of_d=float(lst2[1])*float(lst[0])
        #

        #store exact value of the length <a>=height <b>=base <c>=hypotenuse which mention, convert to 100 unit (taking 2 decimal point)
        a=int(round(float(raw_data_of_a)*100,0))
        b=int(round(float(raw_data_of_b)*100,0))
        c=sqrt(a**2+b**2)#distance formula
        #

        #calculating alpha <A> and beta <B> angles. <C> always 90 degree.
        C=90
        A=asin(a/c)/pi*180
        B=asin(b/c)/pi*180
        #

        #Due to coding purpose, duplicate one more set variable for further use. Serve as a static reference. i.e. save a set of original data
        a2=int(round(float(raw_data_of_c),2)*100)
        b2=int(round(float(raw_data_of_d),2)*100)
        c2=sqrt(a2**2+b2**2)
        C2=90
        A2=asin(a2/c2)/pi*180
        B2=asin(b2/c2)/pi*180
        #

        #this is the id for svg file tracking purpose, output svg file will have this file_name_id for tracking, format:
        #[numerator_of_left_part]_[denominator_of_left_part]_[numerator_of_right_part]_[denominator_of_right_part] 
        file_name_id=str(lst[0]) + '_' + str(lst[1]) + '_' + str(lst2[0]) + '_' + str(lst2[1])
        #
        #taken the last block as file name

        #A general function to pop out the first value in the given lst and check if the value equal to 1, return True, else return False
        def ud(lst):
            if lst.pop(0)==1:
                return True
            else:
                return False
        #


        ###Different Generator Function for Different Mode
        def ALL_MODE_TRANSPARENCY_GENERATOR(need_twist):
            #iterating for each crease: total crease=int(current_block_total_number_of_column)*int(current_block_total_number_of_row)*9, i.e. total MARROW units * 9 crease for each MARROW units
            for i in range(int(current_block_total_number_of_column)*int(current_block_total_number_of_row)*9):
                if facet!='Facet'and i>int(current_block_total_number_of_column)*int(current_block_total_number_of_row)*6-1:
                    continue
                #create initial lst with all value of 1.
                lstoftransparency_crease_index=[]
                for j in range(10000):
                    lstoftransparency_crease_index.append(1)
                #

                #If twist, all <base> creases transparent, create lst for transparency crease (twist), 0 for transparent.turn base crease respective value from 1 to 0.
                if need_twist:
                    for k in range(10000):
                        if k==0:
                            lstoftransparency_crease_index[k]=0
                        else:
                            if k%3==0:
                                lstoftransparency_crease_index[k]=0   
                #


                #if Facet,
                if facet=='Facet':
                    facet_crease_index=[]
                    m=int(current_block_total_number_of_column)*9-2
                    for ii in range(int(current_block_total_number_of_row)):
                        facet_crease_index.append(m)
                        m+=int(current_block_total_number_of_column)*9
                    mm=9*(int(current_block_total_number_of_row)-1)*int(current_block_total_number_of_column)+1
                    c=0
                    for k in range(int(current_block_total_number_of_column)*2):
                        if c%2==0:
                            facet_crease_index.append(mm)
                            mm+=5
                        if c%2==1:
                            facet_crease_index.append(mm)
                            mm+=4
                        c+=1

                    #if specific crease transparency, turn specific crease value from 1 to 0.
                    for kk in facet_crease_index:
                        lstoftransparency_crease_index[kk]=0   
                    #                
                else:
                    #If no facet,
                    facet_crease_index=[]
                    m=int(current_block_total_number_of_column)*6-2
                    for ii in range(int(current_block_total_number_of_row)):
                        facet_crease_index.append(m)
                        m+=int(current_block_total_number_of_column)*6
                    mm=6*(int(current_block_total_number_of_row)-1)*int(current_block_total_number_of_column)
                    for k in range(int(current_block_total_number_of_column)*2):
                        facet_crease_index.append(mm)
                        mm+=3
                    #

                    #if specific crease transparency, turn specific crease value from 1 to 0.
                    for kk in facet_crease_index:
                        lstoftransparency_crease_index[kk]=0
                    #
                
                #No specific transparency crease, only iterating crease is transparency, i.e. crease ith=0
                lstoftransparency_crease_index[i]=0
                #

                #Layout setting and axes format
                ax='a'+str(i)
                if facet=='Facet':
                    ax = f1.add_subplot(int(current_block_total_number_of_column)*3,int(current_block_total_number_of_row)*3,i+1)
                    ax.axis('off')
                else:
                    ax = f1.add_subplot(int(current_block_total_number_of_column)*2,int(current_block_total_number_of_row)*3,i+1)#int(current_block_total_number_of_column)*2,int(current_block_total_number_of_row)*3,i+1
                    ax.axis('off')
                    ax.set_aspect('equal', adjustable='box')
                    ax.spines['bottom'].set_color('#FFFFFFFF')
                    ax.spines['top'].set_color('#FFFFFFFF')
                    ax.spines['left'].set_color('#FFFFFFFF')
                    ax.spines['right'].set_color('#FFFFFFFF')
                #
                
                ###Module of the unit <m1>=left part of MARROW unit, <m2>=right part of MARROW unit, <m3>=integrate <m1> and <m2> with the outer frame
                def m2(origin,lstofopacity):
                    x=origin[-2]
                    y=origin[-1]
                    if facet=="Facet":
                        x0=x+b2
                        y0=y+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                        color0='#FF0000'+lstofopacity.pop(0)
                        x1=[x0,x0-b2]
                        y1=[y,y0]
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x1,y1,color=color0,linewidth=line_width)
                    if facet=="Facet":
                        color1='#FFFF00'+lstofopacity.pop(0)
                    else:
                        color1='#FF0000'+lstofopacity.pop(0)
                    x+=b2
                    x1=[x-b2,x]
                    y1=[y,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color1,linewidth=line_width)
                    color2='#FF0000'+lstofopacity.pop(0)
                    y+=a
                    x1=[x,x]
                    y1=[y-a,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color2,linewidth=line_width)
                    y-=a2  
                    color3='#0000FF'+lstofopacity.pop(0)
                    y+=a2
                    x-=b2
                    x1=[x+b2,x]
                    y1=[y-a2,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color3,linewidth=line_width)
                    y-=a2
                    x1=[x,x]
                    y1=[y,y+a2]
                    x+=b2
                    origin.append(x)
                    origin.append(y)
                    return origin
                def m1(origin,lstofopacity):
                    x=origin[-2]
                    y=origin[-1]
                    if facet=="Facet":
                        x0=x+b
                        y0=y+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                        color0='#FF0000'+lstofopacity.pop(0)
                        x1=[x0-b,x0]
                        y1=[y,y0]
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x1,y1,color=color0,linewidth=line_width)
                    if facet=="Facet":
                        color1='#FFFF00'+lstofopacity.pop(0)
                    else:
                        color1='#FF0000'+lstofopacity.pop(0)
                    x+=b
                    x1=[x-b,x]
                    y1=[y,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color1,linewidth=line_width)
                    color2='#FF0000'+lstofopacity.pop(0)
                    if facet=='Facet':
                        y+=sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                        x0=[x,x]
                        y0=[y-sin(facet_angle)/sin(90/180*pi-facet_angle)*b2,y]
                        color4='#0000FF'+lstofopacity.pop(0)
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x0,y0,color=color4,linewidth=line_width)
                        y+=a-sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                        x1=[x,x]
                        y1=[y-a+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2,y]
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x1,y1,color=color2,linewidth=line_width)
                    else:
                        y+=a
                        x1=[x,x]
                        y1=[y-a,y]
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x1,y1,color=color2,linewidth=line_width)
                    color3='#0000FF'+lstofopacity.pop(0)
                    x-=b
                    y-=a
                    x1=[x,x+b]
                    y1=[y,y+a]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color3,linewidth=line_width)
                    x+=b
                    origin.append(x)
                    origin.append(y)
                    return origin
                def m3(row,repeat,origin,lstofopacity):
                    idx=0
                    for j in range(row):
                        for iii in range(repeat):
                            m1(origin,lstofopacity)
                            m2(origin,lstofopacity)
                        if idx!=row-1:
                            x=origin[-2]
                            y=origin[-1]
                            origin.append(x-repeat*b-repeat*b2) 
                            origin.append(y-a) 
                        idx+=1
                    colorf='#000000FF'
                    x=origin[-2]
                    y=origin[-1]
                    y+=row*(a)
                    x1=[x,x]
                    y1=[y-row*(a),y]
                    ax.plot(x1,y1,color=colorf,linewidth=line_width)
                    x-=repeat*(b+b2)
                    x1=[x+repeat*(b+b2),x]
                    y1=[y,y]
                    ax.plot(x1,y1,color=colorf,linewidth=line_width)
                    y-=row*(a)
                    x1=[x,x]
                    y1=[y+row*(a),y]
                    ax.plot(x1,y1,color=colorf,linewidth=line_width)
                    x+=repeat*(b+b2)
                    x1=[x-repeat*(b+b2),x]
                    y1=[y,y]
                    ax.plot(x1,y1,color=colorf,linewidth=line_width)
                    return origin
                ### These modules is specific for MARROW structure, using different x and y value to draw MARROW unit.
                
                origin=[0,0]#origin x=0, y=0
                #create a initial lst of opacity with all 'FF' hex opacity code, which is 100% opacity
                lstofopacity=[]
                for k in range(10000):
                    lstofopacity.append('FF')
                #

                #Call <m3> function with info below.
                m3(int(current_block_total_number_of_row),int(current_block_total_number_of_column),origin,lstofopacity)

        def GENERAL_MARROW_GENERATOR(lstofspecific_block_index_and_opacity,lstofspecific_transparencyblock_index,need_twist):   #lstofspecific_block_index_and_opacity,lstofspecific_transparencyblock_index,need_twist 
            #create initial lst with all value of 1.
            lstoftransparency_crease_index=[]
            for j in range(10000):
                lstoftransparency_crease_index.append(1)
            #

            #If twist, all <base> creases transparent, create lst for transparency crease (twist), 0 for transparent.turn base crease respective value from 1 to 0.
            if need_twist:
                for k in range(10000):
                    if k==0:
                        lstoftransparency_crease_index[k]=0
                    else:
                        if k%3==0:#<base> creases always satisfied index divided by 3 with no remainder 
                            lstoftransparency_crease_index[k]=0    
            #

            #if Facet,
            if facet=='Facet':
                facet_crease_index=[]
                m=int(current_block_total_number_of_column)*9-2
                for ii in range(int(current_block_total_number_of_row)):
                    facet_crease_index.append(m)
                    m+=int(current_block_total_number_of_column)*9
                mm=9*(int(current_block_total_number_of_row)-1)*int(current_block_total_number_of_column)+1
                c=0
                for k in range(int(current_block_total_number_of_column)*2):
                    if c%2==0:
                        facet_crease_index.append(mm)
                        mm+=5
                    if c%2==1:
                        facet_crease_index.append(mm)
                        mm+=4
                    c+=1

                #if specific crease transparency, turn specific crease value from 1 to 0.
                for kk in facet_crease_index:
                    lstoftransparency_crease_index[kk]=0     
                #              
            else:
                #If no facet,
                facet_crease_index=[]
                m=int(current_block_total_number_of_column)*6-2
                for ii in range(int(current_block_total_number_of_row)):
                    facet_crease_index.append(m)
                    m+=int(current_block_total_number_of_column)*6
                mm=6*(int(current_block_total_number_of_row)-1)*int(current_block_total_number_of_column)
                for k in range(int(current_block_total_number_of_column)*2):
                    facet_crease_index.append(mm)
                    mm+=3
                #

                #if specific crease transparency, turn specific crease value from 1 to 0.
                for kk in facet_crease_index:
                    lstoftransparency_crease_index[kk]=0
                #

            #if specific crease transparency, turn specific crease value from 1 to 0.
            for i in lstofspecific_transparencyblock_index:
                lstoftransparency_crease_index[i]=0
            #

            #Layout setting and axes format
            ax='a'+str(current_block_index)
            ax = f1.add_subplot(layout_number_of_rows,layout_number_of_columns+1,1+current_block_index)
            ax.axis('off')
            print(layout_number_of_rows)
            print(layout_number_of_columns)
            print('subplot'+str(current_block_index))
            ax.set_aspect('equal', adjustable='box')
            ax.spines['bottom'].set_color('#FFFFFFFF')
            ax.spines['top'].set_color('#FFFFFFFF')
            ax.spines['left'].set_color('#FFFFFFFF')
            ax.spines['right'].set_color('#FFFFFFFF')
            #

            ###Module of the unit <m1>=left part of MARROW unit, <m2>=right part of MARROW unit, <m3>=integrate <m1> and <m2> with the outer frame
            def m2(origin,lstofopacity):
                x=origin[-2]
                y=origin[-1]
                if facet=="Facet":
                    x0=x+b2
                    y0=y+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                    color0='#FF0000'+lstofopacity.pop(0)
                    x1=[x0,x0-b2]
                    y1=[y,y0]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color0,linewidth=line_width)
                if facet=="Facet":
                    color1='#FFFF00'+lstofopacity.pop(0)
                else:
                    color1='#FF0000'+lstofopacity.pop(0)
                x+=b2
                x1=[x-b2,x]
                y1=[y,y]
                if ud(lstoftransparency_crease_index):
                    ax.plot(x1,y1,color=color1,linewidth=line_width)
                color2='#FF0000'+lstofopacity.pop(0)
                y+=a
                x1=[x,x]
                y1=[y-a,y]
                if ud(lstoftransparency_crease_index):
                    ax.plot(x1,y1,color=color2,linewidth=line_width)
                y-=a2  
                color3='#0000FF'+lstofopacity.pop(0)
                y+=a2
                x-=b2
                x1=[x+b2,x]
                y1=[y-a2,y]
                if ud(lstoftransparency_crease_index):
                    ax.plot(x1,y1,color=color3,linewidth=line_width)
                y-=a2
                x1=[x,x]
                y1=[y,y+a2]
                x+=b2
                origin.append(x)
                origin.append(y)
                return origin
            def m1(origin,lstofopacity):
                x=origin[-2]
                y=origin[-1]
                if facet=="Facet":
                    x0=x+b
                    y0=y+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                    color0='#FF0000'+lstofopacity.pop(0)
                    x1=[x0-b,x0]
                    y1=[y,y0]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color0,linewidth=line_width)
                if facet=="Facet":
                    color1='#FFFF00'+lstofopacity.pop(0)
                else:
                    color1='#FF0000'+lstofopacity.pop(0)
                x+=b
                x1=[x-b,x]
                y1=[y,y]
                if ud(lstoftransparency_crease_index):
                    ax.plot(x1,y1,color=color1,linewidth=line_width)
                color2='#FF0000'+lstofopacity.pop(0)
                if facet=='Facet':
                    y+=sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                    x0=[x,x]
                    y0=[y-sin(facet_angle)/sin(90/180*pi-facet_angle)*b2,y]
                    color4='#0000FF'+lstofopacity.pop(0)
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x0,y0,color=color4,linewidth=line_width)
                    y+=a-sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                    x1=[x,x]
                    y1=[y-a+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color2,linewidth=line_width)
                else:
                    y+=a
                    x1=[x,x]
                    y1=[y-a,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color2,linewidth=line_width)
                color3='#0000FF'+lstofopacity.pop(0)
                x-=b
                y-=a
                x1=[x,x+b]
                y1=[y,y+a]
                if ud(lstoftransparency_crease_index):
                    ax.plot(x1,y1,color=color3,linewidth=line_width)
                x+=b
                origin.append(x)
                origin.append(y)
                return origin
            def m3(row,repeat,origin,lstofopacity):
                idx=0
                for j in range(row):
                    for iii in range(repeat):
                        m1(origin,lstofopacity)
                        m2(origin,lstofopacity)
                    if idx!=row-1:
                        x=origin[-2]
                        y=origin[-1]
                        origin.append(x-repeat*b-repeat*b2) 
                        origin.append(y-a) 
                    idx+=1
                colorf='#000000FF'
                x=origin[-2]
                y=origin[-1]
                y+=row*(a)
                x1=[x,x]
                y1=[y-row*(a),y]
                ax.plot(x1,y1,color=colorf,linewidth=line_width)
                x-=repeat*(b+b2)
                x1=[x+repeat*(b+b2),x]
                y1=[y,y]
                ax.plot(x1,y1,color=colorf,linewidth=line_width)
                y-=row*(a)
                x1=[x,x]
                y1=[y+row*(a),y]
                ax.plot(x1,y1,color=colorf,linewidth=line_width)
                x+=repeat*(b+b2)
                x1=[x-repeat*(b+b2),x]
                y1=[y,y]
                ax.plot(x1,y1,color=colorf,linewidth=line_width)
                return origin
            ### These modules is specific for MARROW structure, using different x and y value to draw MARROW unit.

            origin=[0,0]#origin x=0, y=0
            #create a initial lst of opacity with all 'FF' hex opacity code, which is 100% opacity
            lstofopacity=[]
            for k in range(10000):
                lstofopacity.append('FF')
            #

            #Change the opacity value from FF to specific hex opacity code
            if len(lstofspecific_block_index_and_opacity)!=0:
                for j in lstofspecific_block_index_and_opacity:
                    idx=int(j[0])
                    lstofopacity[idx]=j[1]
            #
            
            #Call <m3> function with info below.
            m3(int(current_block_total_number_of_row),int(current_block_total_number_of_column),origin,lstofopacity)

        def ALL_MODE_OPACITY_GENERATOR(current_block_opcaity_for_All_mode,need_twist,line_width):
            #iterating for each crease: total crease=int(current_block_total_number_of_column)*int(current_block_total_number_of_row)*9, i.e. total MARROW units * 9 crease for each MARROW units
            for i in range(int(current_block_total_number_of_column)*int(current_block_total_number_of_row)*9):
                if facet!='Facet'and i>int(current_block_total_number_of_column)*int(current_block_total_number_of_row)*6-1:
                    continue 
                #create initial lst with all value of 1.
                lstoftransparency_crease_index=[]
                for j in range(10000):
                    lstoftransparency_crease_index.append(1)
                #

                #If twist, all <base> creases transparent, create lst for transparency crease (twist), 0 for transparent.turn base crease respective value from 1 to 0.
                if need_twist:
                    for k in range(10000):
                        if k==0:
                            lstoftransparency_crease_index[k]=0
                        else:
                            if k%3==0:
                                lstoftransparency_crease_index[k]=0   
                #

                #if Facet,   
                if facet=='Facet':
                    facet_crease_index=[]
                    m=int(current_block_total_number_of_column)*9-2
                    for ii in range(int(current_block_total_number_of_row)):
                        facet_crease_index.append(m)
                        m+=int(current_block_total_number_of_column)*9
                    mm=9*(int(current_block_total_number_of_row)-1)*int(current_block_total_number_of_column)+1
                    c=0
                    for k in range(int(current_block_total_number_of_column)*2):
                        if c%2==0:
                            facet_crease_index.append(mm)
                            mm+=5
                        if c%2==1:
                            facet_crease_index.append(mm)
                            mm+=4
                        c+=1

                    #if specific crease transparency, turn specific crease value from 1 to 0.
                    for kk in facet_crease_index:
                        lstoftransparency_crease_index[kk]=0   
                    #                
                else:
                    #If no facet,
                    facet_crease_index=[]
                    m=int(current_block_total_number_of_column)*6-2
                    for ii in range(int(current_block_total_number_of_row)):
                        facet_crease_index.append(m)
                        m+=int(current_block_total_number_of_column)*6
                    mm=6*(int(current_block_total_number_of_row)-1)*int(current_block_total_number_of_column)
                    for k in range(int(current_block_total_number_of_column)*2):
                        facet_crease_index.append(mm)
                        mm+=3
                    #

                    #if specific crease transparency, turn specific crease value from 1 to 0.
                    for kk in facet_crease_index:
                        lstoftransparency_crease_index[kk]=0
                    #
                
                #Layout setting and axes format
                ax='a'+str(i)
                if facet=='Facet':
                    ax = f1.add_subplot(int(current_block_total_number_of_column)*3,int(current_block_total_number_of_row)*3,i+1)
                    ax.axis('off')
                else:
                    ax = f1.add_subplot(int(current_block_total_number_of_column)*2,int(current_block_total_number_of_row)*3,i+1)#int(current_block_total_number_of_column)*2,int(current_block_total_number_of_row)*3,i+1
                    ax.axis('off')
                ax.set_aspect('equal', adjustable='box')
                ax.spines['bottom'].set_color('#FFFFFFFF')
                ax.spines['top'].set_color('#FFFFFFFF')
                ax.spines['left'].set_color('#FFFFFFFF')
                ax.spines['right'].set_color('#FFFFFFFF')
                #

                ###Module of the unit <m1>=left part of MARROW unit, <m2>=right part of MARROW unit, <m3>=integrate <m1> and <m2> with the outer frame
                def m2(origin,lstofopacity,line_width):
                    line_width=line_width
                    x=origin[-2]
                    y=origin[-1]
                    if facet=="Facet":
                        x0=x+b2
                        y0=y+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                        color0='#FF0000'+lstofopacity.pop(0)
                        x1=[x0,x0-b2]
                        y1=[y,y0]
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x1,y1,color=color0,linewidth=line_width)
                    if facet=="Facet":
                        color1='#FFFF00'+lstofopacity.pop(0)
                    else:
                        color1='#FF0000'+lstofopacity.pop(0)
                    x+=b2
                    x1=[x-b2,x]
                    y1=[y,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color1,linewidth=line_width)
                    color2='#FF0000'+lstofopacity.pop(0)
                    y+=a
                    x1=[x,x]
                    y1=[y-a,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color2,linewidth=line_width)
                    y-=a2  
                    color3='#0000FF'+lstofopacity.pop(0)
                    y+=a2
                    x-=b2
                    x1=[x+b2,x]
                    y1=[y-a2,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color3,linewidth=line_width)
                    y-=a2
                    x1=[x,x]
                    y1=[y,y+a2]
                    x+=b2
                    origin.append(x)
                    origin.append(y)
                    return origin
                def m1(origin,lstofopacity,line_width):
                    line_width=line_width
                    x=origin[-2]
                    y=origin[-1]
                    if facet=="Facet":
                        x0=x+b
                        y0=y+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                        color0='#FF0000'+lstofopacity.pop(0)
                        x1=[x0-b,x0]
                        y1=[y,y0]
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x1,y1,color=color0,linewidth=line_width)
                    if facet=="Facet":
                        color1='#FFFF00'+lstofopacity.pop(0)
                    else:
                        color1='#FF0000'+lstofopacity.pop(0)
                    x+=b
                    x1=[x-b,x]
                    y1=[y,y]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color1,linewidth=line_width)
                    color2='#FF0000'+lstofopacity.pop(0)
                    if facet=='Facet':
                        y+=sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                        x0=[x,x]
                        y0=[y-sin(facet_angle)/sin(90/180*pi-facet_angle)*b2,y]
                        color4='#0000FF'+lstofopacity.pop(0)
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x0,y0,color=color4,linewidth=line_width)
                        y+=a-sin(facet_angle)/sin(90/180*pi-facet_angle)*b2
                        x1=[x,x]
                        y1=[y-a+sin(facet_angle)/sin(90/180*pi-facet_angle)*b2,y]
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x1,y1,color=color2,linewidth=line_width)
                    else:
                        y+=a
                        x1=[x,x]
                        y1=[y-a,y]
                        if ud(lstoftransparency_crease_index):
                            ax.plot(x1,y1,color=color2,linewidth=line_width)
                    color3='#0000FF'+lstofopacity.pop(0)
                    x-=b
                    y-=a
                    x1=[x,x+b]
                    y1=[y,y+a]
                    if ud(lstoftransparency_crease_index):
                        ax.plot(x1,y1,color=color3,linewidth=line_width)
                    x+=b
                    origin.append(x)
                    origin.append(y)
                    return origin
                def m3(row,repeat,origin,lstofopacity,line_width):
                    idx=0
                    for j in range(row):
                        for iii in range(repeat):
                            m1(origin,lstofopacity,line_width)
                            m2(origin,lstofopacity,line_width)
                        if idx!=row-1:
                            x=origin[-2]
                            y=origin[-1]
                            origin.append(x-repeat*b-repeat*b2) 
                            origin.append(y-a) 
                        idx+=1
                    line_width=line_width
                    colorf='#000000FF'
                    x=origin[-2]
                    y=origin[-1]
                    y+=row*(a)
                    x1=[x,x]
                    y1=[y-row*(a),y]
                    ax.plot(x1,y1,color=colorf,linewidth=line_width)
                    x-=repeat*(b+b2)
                    x1=[x+repeat*(b+b2),x]
                    y1=[y,y]
                    ax.plot(x1,y1,color=colorf,linewidth=line_width)
                    y-=row*(a)
                    x1=[x,x]
                    y1=[y+row*(a),y]
                    ax.plot(x1,y1,color=colorf,linewidth=line_width)
                    x+=repeat*(b+b2)
                    x1=[x-repeat*(b+b2),x]
                    y1=[y,y]
                    ax.plot(x1,y1,color=colorf,linewidth=line_width)
                    return origin
                ### These modules is specific for MARROW structure, using different x and y value to draw MARROW unit.
                
                origin=[0,0]#origin x=0, y=0
                #create a initial lst of opacity with all 'FF' hex opacity code, which is 100% opacity
                lstofopacity=[]
                for k in range(10000):
                    lstofopacity.append('FF')
                #

                #No specific transparency crease, only iterating crease is transparency, i.e. crease ith=user input value
                lstofopacity[i]=odic[current_block_opcaity_for_All_mode]
                #

                #Call <m3> function with info below.
                m3(int(current_block_total_number_of_row),int(current_block_total_number_of_column),origin,lstofopacity,line_width)

        ###

        ##Process via Specific of Mode: <No>=normal mode, <All>=iterative crease opacity mode, <Specific>=specific crease opacity mode
        #if <All> mode be selected
        if current_block_choice_ratio_or_angle=='All':
            current_block_opcaity_for_All_mode=lstofforallopacity.pop(0)#store the opacity which need to apply in <All> mode
            #if opacity of <All> mode is 0, i.e. fully transparency, call ALL_MODE_TRANSPARENCY_GENERATOR
            if current_block_opcaity_for_All_mode=='0':
                ALL_MODE_TRANSPARENCY_GENERATOR(need_twist)
            #
            #if opacity of <All> mode is not 0, i.e. partially transparency, call ALL_MODE_OPACITY_GENERATOR with opacity info lsts.
            else:
                ALL_MODE_OPACITY_GENERATOR(current_block_opcaity_for_All_mode,need_twist,line_width)
            #
        #
        
        #if <No> mode be selected
        if current_block_choice_ratio_or_angle=='No':
            GENERAL_MARROW_GENERATOR([],[],need_twist)#Use GENERAL_MARROW_GENERATOR with empty transparency and opacity lst
        #

        #if <Specific> mode be selected
        if current_block_choice_ratio_or_angle=='Specific':
            ##retrieve specific block transparency/opacity info (index and opacity level)
            lstofspecific_block_index_and_opacity=[]
            lstofspecific_transparencyblock_index=[]
            #retrieve transparency info (index)
            while True:
                if len(lstofsptrans)==0:
                    break
                specific_transparencyblock_index=lstofsptrans.pop(0)
                lstofspecific_transparencyblock_index.append(int(specific_transparencyblock_index))
            #

            #retrieve opacity info (index and opacity level)
            while True:
                if len(lstofspopaci)==0:
                    break
                specific_block_index=lstofspopaci.pop(0)
                specific_block_opacity=lstofspopaci.pop(0)
                lstofspecific_block_index_and_opacity.append([specific_block_index,odic[specific_block_opacity]])#Recap: odic=opacity dictionary,odic[specific_block_opacity] is convert level of opacity in x % into hex opacity code format
            #

            ##
            GENERAL_MARROW_GENERATOR(lstofspecific_block_index_and_opacity,lstofspecific_transparencyblock_index,need_twist)#call GENERAL_MARROW_GENERATOR function with info lsts.
        #
        ##
    #Output
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()#show all blocks (svg file preview)
    filename=filenames+ '.svg' # 'MARROW' +'_'+ current_block_total_number_of_row + '_' + current_block_total_number_of_column +'_'+ file_name_id+ '.svg' File name format: 'MARROW_[current_block_total_number_of_row]_[current_block_total_number_of_column]_[file_name_id].svg'
    f1.savefig(filename, bbox_inches=0, transparent=True) #save file with file name mentioned above


####
#Only edit here
filenames='SpecificFunction25'
Excelfilename=filenames+'.csv'

#read excel file 'Auto-Generating System' file and 'hexcode' file
opacity=read_csv('hexcode.csv')
odic={} #opacity dictionary. 
for i in opacity[1::]:
    odic[i[0]]=i[1]#key: x % opacity, value is the hex opacity code 

excelorderdata=read_csv(Excelfilename)#extract excel data
#

#extract line width from excel data
line_width_raw_data=excelorderdata[0][2]
line_width=float(line_width_raw_data)
#

MARROW_STRUCTURE_GENERATOR()#Call function


#YX-20200805 version