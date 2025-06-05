import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from tkmacosx import Button
import forecast_faster as fc
import setting

#Global Variable
chem_name = 'unnamed'
training_size = 0.7
Fitted_Model = []
RawData = pd.DataFrame()
TestingData = pd.DataFrame()
OutcomeData = pd.DataFrame()
RecommendedModel = 0
CurrentPage = 0
Model_Selected = setting.Models[0] #這邊之後要在分析完之後更新

"""
按鍵指令
"""
#################    各種continue鍵指令    ################# 
def StartCmd():
    global chem_name
    chem_name = chem_entry.get()
    show_data_name['text'] = chem_name
    menu_frame.tkraise()
    input_frame_left.tkraise()
    input_frame_right.tkraise()
    global CurrentPage
    CurrentPage = 1
    print(chem_name)

def InputPageCtnCmd():
    
    #TODO: 開始預測
    global Fitted_Model
    Fitted_Model.append(fc.output(RawData, training_size)) #forecast class
    Fitted_Model.append(Fitted_Model[0].error_chart()) #dataframe of MAPE
    #推薦model
    RecommendedModel = Fitted_Model[0].best_model()
    b_select_model[RecommendedModel].configure(bg = setting.recommended_model_color)

    #畫barchart
    Fitted_Model[0].bar_chart(Fitted_Model[1])
    img = Image.open("plot.png").convert("RGB")
    img = img.resize((400, 400))
    tkimage = ImageTk.PhotoImage(img)
    #img_label = tk.Label(models_frame_right, image=tkimage).place(anchor=tk.CENTER, x = (600-setting.menu_height)/2, y = (800-setting.left_side_width)/2)
    img_label = tk.Label(models_frame_right, image = tkimage)
    img_label.image = tkimage
    img_label.place(anchor=tk.CENTER, x = (600-setting.menu_height)/2, y = (800-setting.left_side_width)/2)
    
    #換頁指令
    models_frame_left.tkraise()
    models_frame_right.tkraise()
    global CurrentPage
    CurrentPage = 2

    print('---InputPageCtnCmd---')

def ModelsPageCtnCmd():
    predict_frame_left.tkraise()
    predict_frame_right.tkraise()
    global CurrentPage
    CurrentPage = 3
    print('---ModelsPageCtnCmd---')

def PredictPageCtnCmd():
    outcome_frame_all.tkraise()
    outcome_frame_mid.tkraise()
    global CurrentPage
    CurrentPage = 4
    #TODO:
    global OutcomeData
    global TestingData
    global Model_Selected
    OutcomeData = Fitted_Model[0].forecast_result(TestingData, Model_Selected)
    ###
    MakeOutcomeDataTree(OutcomeData)
    ###
    print('---PredictPageCtnCmd---')

def RestartCmd():
    global chem_name
    global training_size
    global RawData
    global TestingData
    global OutcomeData
    global CurrentPage
    global Model_Selected
    chem_name = 'unnamed'
    training_size = 0.7
    RawData = pd.DataFrame()
    TestingData = pd.DataFrame()
    OutcomeData = pd.DataFrame()
    CurrentPage = 0
    Model_Selected = setting.Models[0]
    cover_frame.tkraise()
    print('---RestartCmd---')

#################    畫資料圖指令    ################# 

def MakeTree(df):
    global RawDataTree
    RawDataTree = ttk.Treeview.destroy
    RawDataTree = ttk.Treeview(input_frame_right)
    df_cols = df.columns.values.tolist()
    print(df_cols)
    RawDataTree['columns'] = df_cols
    RawDataTree.column("#0", anchor=tk.CENTER, width = 50)
    for i in df_cols:
        RawDataTree.column(i, anchor=tk.CENTER, width = int((600-setting.menu_height-70)/len(df_cols)))
        RawDataTree.heading(i, text = i, anchor=tk.CENTER)
    for index, row in df.iterrows():
        RawDataTree.insert("", 'end', text = index, values = list(row))
    RawDataTree.place(anchor=tk.CENTER, x = (600-setting.menu_height)/2, y = (800-setting.left_side_width)/2)

def MakeTestingTree(df):
    global TestingDataTree
    TestingDataTree = ttk.Treeview.destroy
    TestingDataTree = ttk.Treeview(predict_frame_right)
    df_cols = df.columns.values.tolist()
    print(df_cols)
    TestingDataTree['columns'] = df_cols
    TestingDataTree.column("#0", anchor=tk.CENTER, width = 50)
    for i in df_cols:
        TestingDataTree.column(i, anchor=tk.CENTER, width = int((600-setting.menu_height-70)/len(df_cols)))
        TestingDataTree.heading(i, text = i, anchor=tk.CENTER)
    for index, row in df.iterrows():
        TestingDataTree.insert("", 'end', text = index, values = list(row))
    TestingDataTree.place(anchor=tk.CENTER, x = (600-setting.menu_height)/2, y = (800-setting.left_side_width)/2)

def MakeOutcomeDataTree(df):
    global OutcomeDataTree
    OutcomeDataTree = ttk.Treeview.destroy
    OutcomeDataTree = ttk.Treeview(outcome_frame_mid)
    df_cols = df.columns.values.tolist()
    print(df_cols)
    OutcomeDataTree['columns'] = df_cols
    OutcomeDataTree.column("#0", anchor=tk.CENTER, width = 50)
    for i in df_cols:
        OutcomeDataTree.column(i, anchor=tk.CENTER, width = int((600-setting.menu_height-70)/len(df_cols)))
        OutcomeDataTree.heading(i, text = i, anchor=tk.CENTER)
    for index, row in df.iterrows():
        OutcomeDataTree.insert("", 'end', text = index, values = list(row))
    OutcomeDataTree.place(anchor=tk.CENTER, x = 750/2, y = (600-setting.menu_height-125)/2)

#################    讀寫資料指令    ################# 

def InputDataCmd():
    print('---InputDataCmd---')
    global RawData
    FL = askopenfilename(parent = window, title = '選取資料', filetypes = [("Excel files", ".xlsx .xls"), ("csv file", ".csv")])
    if FL.split(".")[1] in ["xlsx", "xls"]:
        RawData = pd.DataFrame(pd.read_excel(FL))
        MakeTree(RawData)
        print('excel file uploaded!')
    elif FL.split(".")[1] in ["csv"]:
        RawData = pd.DataFrame(pd.read_csv(FL))
        MakeTree(RawData)
        print('csv file uploaded!')
    #else: message 錯誤資料格式請重新選取資料

def InputTestingDataCmd():
    print('---InputTestingDataCmd---')
    global TestingData
    FL = askopenfilename(parent = window, title = '選取資料')
    if FL.split(".")[1] in ["xlsx", "xls"]:
        TestingData = pd.DataFrame(pd.read_excel(FL))
        MakeTestingTree(TestingData)
        print('excel file uploaded!')
    elif FL.split(".")[1] in ["csv"]:
        TestingData = pd.DataFrame(pd.read_csv(FL))
        MakeTestingTree(TestingData)
        print('csv file uploaded!')
    #else: message 錯誤資料格式請重新選取資料

def DownloadDataCmd():
    FL = asksaveasfilename(parent = window, title = '儲存檔案為',filetypes=(("Excel .xlsx", "Excel .xls")))
    if FL:
        OutcomeData.to_excel(FL+".xlsx", index=False, sheet_name="Results") 
    print('---DownloadDataCmd---')
#################    其他指令    ################# 

def TrainingSetCmd(event):
    global training_size
    training_size = TS_clicked.get()
    print('---TrainigSetCmd---')
    print('Training Size = ' + str(training_size))

#################    menu鍵指令    ################# 

def MenuCmd_input():
    global CurrentPage
    if CurrentPage > 1:
        StartCmd()
    print('---MenuCmd_input---')

def MenuCmd_model():
    global CurrentPage
    if CurrentPage > 2:
        InputPageCtnCmd()
    print('---MenuCmd_model---')

def MenuCmd_predict():
    global CurrentPage
    if CurrentPage > 3:
        ModelsPageCtnCmd()
    print('---MenuCmd_predict---')

#################    選模型指令    ################# 

def SelectModel0():
    global Model_Selected
    Model_Selected = setting.Models[0]
    print('---SelectModel0---')
def SelectModel1():
    global Model_Selected
    Model_Selected = setting.Models[1]
    print('---SelectModel1---')
def SelectModel2():
    global Model_Selected
    Model_Selected = setting.Models[2]
    print('---SelectModel2---')
def SelectModel3():
    global Model_Selected
    Model_Selected = setting.Models[3]
    print('---SelectModel3---')
SelectModelCmd = [SelectModel0, SelectModel1, SelectModel2, SelectModel3]


"""
定義視窗
"""

window = tk.Tk()
window.title('Demand Forecaster')
window.geometry('800x600')
window.resizable(False, False)
window.configure(bg = setting.cover_bg_color)
#window.iconbitmap("路徑")

"""
首頁
"""
cover_frame = tk.Frame(window, bg = setting.cover_bg_color, height = 600, width = 800)
cover_frame.place(anchor=tk.CENTER, x = 400, y = 300)

welcome_title = tk.Label(cover_frame, text='Welcome to Demand Forecaster!', bg = setting.cover_bg_color, fg='#FFFFFF', font=(setting.DFfont, 40, 'bold'))
welcome_title.place(anchor=tk.CENTER, x = 400, y = 200)

chem_entry = tk.Entry(cover_frame, bg = 'white', fg = '#000000', font = (setting.DFfont, 30), justify=tk.CENTER)
chem_entry.place(anchor=tk.CENTER, x = 400, y = 300)

b_start = Button(cover_frame, text = 'start', bg = 'LightPink', fg = '#000000', font=(setting.DFfont, 30), command = StartCmd, borderless = 1)
b_start['width'] = 350
b_start['height'] = 40
b_start.place(anchor=tk.CENTER, x = 400, y = 350)

"""
上方進度目錄
"""
menu_frame = tk.Frame(window, bg = setting.cover_bg_color, height = setting.menu_height, width = 800)
menu_frame.place(x = 0, y = 0)
#回輸入頁面
b_input_menu = Button(menu_frame, text = '輸入資料', bg = setting.cover_bg_color, fg = setting.menu_btn_color, font=(setting.DFfont, setting.menu_font_size), command = MenuCmd_input, borderless = 1)
b_input_menu['width'] = setting.menu_btn_width
b_input_menu['height'] = setting.menu_btn_height
b_input_menu.place(anchor=tk.CENTER, x = 80, y = setting.menu_height/2)
#b_input_menu.grid(column = 0, row = 0, padx = 10, pady = 10)

#回model頁面
b_models_menu = Button(menu_frame, text = '選擇模型', bg = setting.cover_bg_color, fg = setting.menu_btn_color, font=(setting.DFfont, setting.menu_font_size), command = MenuCmd_model, borderless = 1)
b_models_menu['width'] = setting.menu_btn_width
b_models_menu['height'] = setting.menu_btn_height
b_models_menu.place(anchor=tk.CENTER, x = 210, y = setting.menu_height/2)
#b_models_menu.grid(column = 1, row = 0, padx = 10, pady = 10)

#回predict頁面
b_predict_menu = Button(menu_frame, text = '輸入預測資料', bg = setting.cover_bg_color, fg = setting.menu_btn_color, font=(setting.DFfont, setting.menu_font_size), command = MenuCmd_predict, borderless = 1)
b_predict_menu['width'] = setting.menu_btn_width+20
b_predict_menu['height'] = setting.menu_btn_height
b_predict_menu.place(anchor=tk.CENTER, x = 350, y = setting.menu_height/2)
#b_predict_menu.grid(column = 2, row = 0, padx = 10, pady = 10)

output_menu = Button(menu_frame, text = '預測結果', bg = setting.cover_bg_color, fg= setting.menu_btn_color, font=(setting.DFfont, setting.menu_font_size), borderless = 1)
output_menu['width'] = setting.menu_btn_width
output_menu['height'] = setting.menu_btn_height
output_menu.place(anchor=tk.CENTER, x = 490, y = setting.menu_height/2)
#output_menu.grid(column = 3, row = 0, padx = 10, pady = 10)

show_data_name = tk.Label(menu_frame, text = chem_name, bg = setting.cover_bg_color, fg= setting.menu_btn_color, font=(setting.DFfont, setting.menu_font_size))
show_data_name.place(anchor=tk.CENTER, x = 720, y = setting.menu_height/2)
#show_data_name.grid(column = 4, row = 0, padx = 10, pady = 10)

"""
輸入資料頁面
"""
#左邊區域
input_frame_left = tk.Frame(window, bg = setting.left_side_color, height = 600-setting.menu_height, width = setting.left_side_width)
input_frame_left.place(x = 0, y = setting.menu_height)

#右邊區域
input_frame_right = tk.Frame(window, bg = setting.right_side_color, height = 600-setting.menu_height, width = 800-setting.left_side_width)
input_frame_right.place(x = setting.left_side_width, y = setting.menu_height)

#資料預覽
RawDataTree = ttk.Treeview(input_frame_right)

#input資料按鍵
b_input_data = Button(input_frame_left, text = '選取資料', bg = setting.normal_button_color, fg = '#000000', font=(setting.DFfont, setting.button_font_size_CHN), command = InputDataCmd, borderless = 1)
b_input_data['width'] = setting.button_width
b_input_data['height'] = setting.button_height
b_input_data.place(anchor=tk.CENTER, x = setting.left_side_width/2, y = (600-setting.menu_height)/2-1.7*setting.button_interval)

#選擇training大小資料按鍵
select_TS_label = tk.Label(input_frame_left, text='選擇訓練集大小', bg = setting.normal_button_color, fg='#000000', font=(setting.DFfont, setting.button_font_size_CHN), height = setting.label_height, width = setting.label_width)
select_TS_label.place(anchor=tk.CENTER, x = setting.left_side_width/2, y = (600-setting.menu_height)/2-0.7*setting.button_interval)

TS_clicked = tk.DoubleVar()
TS_clicked.set(setting.T_options[0])

TS_select = tk.OptionMenu(input_frame_left, TS_clicked, *setting.T_options, command = TrainingSetCmd)
TS_select.config(width = setting.label_width+2, height = setting.label_height)
TS_select.place(anchor=tk.CENTER, x = setting.left_side_width/2, y = (600-setting.menu_height)/2)

#continue
b_ctn1 = Button(input_frame_left, text = 'Continue', bg = setting.ctn_button_color, fg = '#000000', font=(setting.DFfont, setting.button_font_size_ENG), command = InputPageCtnCmd, borderless = 1)
b_ctn1['width'] = setting.button_width
b_ctn1['height'] = setting.button_height
b_ctn1.place(anchor=tk.CENTER, x = setting.left_side_width/2, y = (600-setting.menu_height)/2+setting.button_interval)

"""
預覽model頁面
"""
#左邊區域
models_frame_left = tk.Frame(window, bg = setting.left_side_color, height = 600-setting.menu_height, width = setting.left_side_width)
models_frame_left.place(x = 0, y = setting.menu_height)

#右邊區域
models_frame_right = tk.Frame(window, bg = setting.right_side_color, height = 600-setting.menu_height, width = 800-setting.left_side_width)
models_frame_right.place(x = setting.left_side_width, y = setting.menu_height)

#四個button
b_select_model = []
for i in range(4):
    b_select_model.append(Button())

for i in range(4):
    b_select_model[i] = Button(models_frame_left, text = setting.Models[i], bg = setting.normal_button_color, fg = '#000000', font=(setting.DFfont, setting.button_font_size_CHN), command = SelectModelCmd[i], borderless = 1)
    b_select_model[i]['width'] = setting.button_width
    b_select_model[i]['height'] = setting.button_height
    b_select_model[i].place(anchor=tk.CENTER, x = setting.left_side_width/2, y = (600-setting.menu_height)/2-(2-i)*setting.button_interval)

#continue button
b_ctn2 = Button(models_frame_left, text = 'Continue', bg = setting.ctn_button_color, fg = '#000000', font=(setting.DFfont, setting.button_font_size_ENG), command = ModelsPageCtnCmd, borderless = 1)
b_ctn2['width'] = setting.button_width
b_ctn2['height'] = setting.button_height
b_ctn2.place(anchor=tk.CENTER, x = setting.left_side_width/2, y = (600-setting.menu_height)/2+2*setting.button_interval)

"""
輸入預測資料頁面
"""
#左邊區域
predict_frame_left = tk.Frame(window, bg = setting.left_side_color, height = 600-setting.menu_height, width = setting.left_side_width)
predict_frame_left.place(x = 0, y = setting.menu_height)

#右邊區域
predict_frame_right = tk.Frame(window, bg = setting.right_side_color, height = 600-setting.menu_height, width = 800-setting.left_side_width)
predict_frame_right.place(x = setting.left_side_width, y = setting.menu_height)

#輸入預測資料
TestingDataTree = ttk.Treeview(predict_frame_right)
b_input_test_data = Button(predict_frame_left, text = '選取欲預測之資料', bg = setting.normal_button_color, fg = '#000000', font=(setting.DFfont, setting.button_font_size_CHN), command = InputTestingDataCmd, borderless = 1)
b_input_test_data['width'] = setting.button_width
b_input_test_data['height'] = setting.button_height
b_input_test_data.place(anchor=tk.CENTER, x = setting.left_side_width/2, y = (600-setting.menu_height)/2-setting.button_interval)

#continue button
b_ctn3 = Button(predict_frame_left, text = 'Continue', bg = setting.ctn_button_color, fg = '#000000', font=(setting.DFfont, setting.button_font_size_ENG), command = PredictPageCtnCmd, borderless = 1)
b_ctn3['width'] = setting.button_width
b_ctn3['height'] = setting.button_height
b_ctn3.place(anchor=tk.CENTER, x = setting.left_side_width/2, y = (600-setting.menu_height)/2+setting.button_interval)

"""
結果頁面
"""
#所有區域
outcome_frame_all = tk.Frame(window, bg = setting.right_side_color, height = 600-setting.menu_height, width = 800)
outcome_frame_all.place(x = 0, y = setting.menu_height)

#中間區域
outcome_frame_mid = tk.Frame(window, bg = setting.left_side_color, height = 600-setting.menu_height-125, width = 750)
outcome_frame_mid.place(x = 25, y = setting.menu_height+25)
OutcomeDataTree = ttk.Treeview(outcome_frame_mid)

#輸出資料
b_download_data = Button(outcome_frame_all, text = 'download', bg = setting.normal_button_color, fg = '#000000', font=(setting.DFfont, setting.button_font_size_CHN), command = DownloadDataCmd, borderless = 1)
b_download_data['width'] = setting.button_width
b_download_data['height'] = setting.button_height
b_download_data.place(anchor=tk.CENTER, x = 800/3, y = 500)

#結束按鍵
b_restart = Button(outcome_frame_all, text = '開始預測新的資料', bg = setting.ctn_button_color, fg = '#000000', font=(setting.DFfont, setting.button_font_size_ENG), command = RestartCmd, borderless = 1)
b_restart['width'] = setting.button_width
b_restart['height'] = setting.button_height
b_restart.place(anchor=tk.CENTER, x = 2*800/3, y = 500)

cover_frame.tkraise()
window.mainloop()