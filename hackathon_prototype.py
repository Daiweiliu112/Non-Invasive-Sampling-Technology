from time import strftime
from datetime import *
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import xlsxwriter
from guizero import *
import csv


alarm = [0, 1800]
next_sample=[0,0,0]


def make1():
    alarm[0]=1
    
def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text = string)
    lbl.after(1000,time)
    
def morning_alarm():
    if (alarm[0] == 1):
        print(alarm[0])
        alarm[1] -= 1
        string = ("Take 30 minute sample at "+ str(next_sample[0]) + ":" + str(next_sample[1]) + ":" + str(next_sample[2])+" in " + str(alarm[1]//60) + "min " + str(alarm[1]%60) +"sec")
        lb2.config(text = string)
        lb2.after(1000,morning_alarm)
    else:
        print(alarm[0])
        alarm[1] = 1800
        string = ""
        lb2.config(text = string)
        lb2.after(1000,morning_alarm)

def do_morning_question():
    main_2(1)
     
def do_night_question():
    main_2(0)
    
def close_ex():
    workbook.close()
    
def main_2(alarm_b):
    
    workbook = xlsxwriter.Workbook(str(lst[0][1])+str(lst[0][2])+".xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Question')
    worksheet.set_column('A:A', 50)
    worksheet.set_column('B:Z', 60)

    l1 = [] ## this list temporarily stores the answers
    l2 = [] ## this list is the final list for all of the answers    

    def inc_char(sample):
        i = 65 + sample
        if (i <= 90):
            return chr(i)
        else:
            return chr(90)

    def take_sample(alarm_b):
        data = open("data.txt", "a")
        data.write(str(datetime.now())+",")
        for i in l1:
            data.write(str(i.value)+",")
        data.write("\n")
        data.close()
        temp_list = []
        with open('data.txt', 'r') as data:
            for line in data:
                temp_list.append(line)
        
        for i1 in range(len(temp_list)):
            temp_list2 = temp_list[i1].split(",")
            for i2 in range(len(temp_list2)):
                if (i2 == 0):
                    worksheet.write(str(inc_char(i1+1))+'1', 'Sample '+str(i1)+'   '+str(temp_list2[0]))
                else:
                    worksheet.write(str(inc_char(i1+1))+str(i2+1), temp_list2[i2])
        data.close()
        workbook.close()
        alarm[0] = alarm_b
        if (alarm[0]==1):
            sample_time=datetime.now() + timedelta(minutes=30)  
            next_sample[0] = sample_time.hour
            next_sample[1] = sample_time.minute
            next_sample[2] = sample_time.second

        app.destroy()

        #time_since_wake = s_ans.value
        #print(time_since_wake)
        #future = now - time_since_wake + 10                                          ## countdown function can be seperate than mod_version so that it does not need to be opened for countdown to work.
        #print(future)
        #while time.time() < future:                                                  ## the countdown function then calls the working_version in its own file
        #    pass
        #call (["Python", "working_version.py"])
            
    def slide_ans(ans):
        if (ans == "slide"):
            return True
        else:
            return False
   
    def mult_choice(ans):             
        if (ans == 'mult'):
            return True
        else:
            return False
        
    def given_ans(Str):
        num = ord(Str) - 48                                                          ## change the string to its corresponding number
        li = [f'{row[4]}']
        posn = 5
        while num > 1:
            li.extend([f'{row[posn]}'])
            num -= 1
            posn += 1
        return li

    app = App (title = "NIST", width =480 , height = 320, layout = "grid")
    app.tk.attributes("-fullscreen", True)


    with open('questions.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        q_count = 0
        q_id= 1
        question_col = 2
        
        for row in csv_reader:
            worksheet.write('A'+str(question_col), f'\t{row[1]}') 
            Text(app, text = row[1],
                                grid = [0,q_count], align = "left", color = "blue")
            if (mult_choice(row[2])):                                              ## row[1] is to determine which question it is
                mult_ans = ButtonGroup(app, options = given_ans(row[3]),              ## row[2] is the specification of how many ans
                                    horizontal = True, grid = [0,q_count+1],
                                       align = "left")
                l1.append(mult_ans)
                mult_ans = 0
            elif (slide_ans(row[2])):
                s_ans = Slider (app, start = 0, end = 60, grid = [0,q_count+1])
                l1.append(s_ans)
                s_ans = 0

            else:
                pass
            q_count += 2
            question_col += 1
            
    submit = PushButton(app, text = "Submit", command = lambda: take_sample(alarm_b), grid = [0, q_count + 1], align = "bottom")
    Text(app, text = "Click above to submit",
                        grid = [0,q_count+1], align = "bottom", color = "blue")    
    app.display()

    
root = Tk()
style = Style()
root.title('Home')
root.attributes('-fullscreen', True)
root.geometry("1920x1080")
with open('questions.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    lst = []
    for row in csv_reader:
        lst.append(row)

## background image
background_image = ImageTk.PhotoImage(file = "logo.png")
background_label = Label(root, image = background_image)
background_label.place(x = 0, y = 0, relheight = 1)

## question button
style.configure('W.TButton', font = ('calibri', 30, 'bold', 'underline'), 
                foreground = 'red')
m_q = Button (root,text ='Wake Up Questions',width = 25, command = do_morning_question,
            style = 'W.TButton')
n_q = Button(root, text = 'Sleep Questions', width =25, command = do_night_question,
             style = 'W.TButton')
instruct = Button (root, text ='Instruction', width = 10, command = make1,
                   style ='W.TButton')


#q.pack(side = BOTTOM)                                                           #pack cannot coexist with grid
#q.grid(row = 0, column = 1, pady = 2)
m_q.place(relx = 0.25, x = -2, y = 800, anchor = CENTER)
n_q.place(relx = 0.75, x = -2, y = 800, anchor = CENTER)
instruct.place(relx = 0.92, x = -2, y = 20, anchor = CENTER)

          

## welcome message
style.configure('BW.TLabel', font = ('calibri', 20, 'bold'),
                foreground = 'black', background = 'white')
welcome = Label(root, text = "Welcome " + (lst[0])[1], style = 'BW.TLabel')
welcome.place(relx = 0.5, x = -2, y = 30, anchor = CENTER)
    
lbl = Label(root, font = ('calibri', 30, 'bold'),
                foreground = 'black', background = 'white')
lb2 = Label(root, font = ('calibri', 10, 'bold'),
                foreground = 'black', background = 'white')
lb2.place(relx = 0.5, x = -2, y = 250, anchor = CENTER)
morning_alarm()

lbl.place(relx = 0.5, x = -2, y = 150, anchor = CENTER)
time()

root.mainloop()