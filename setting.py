#字型設計
DFfont = 'Arial'

#背景顏色設計
cover_bg_color = '#364F6B'
left_side_color = '#3FC1C9'
right_side_color = '#E5E5E5'

#配置設計
menu_height = 50
left_side_width = 250

#按鈕設計
button_interval = 50
button_width = 200
button_height = 40
label_width = 16
label_height = 1
button_font_size_CHN = 20
button_font_size_ENG = 20
normal_button_color = '#F5F5F5'
recommended_model_color = '#FFB326'

#continue按鈕設計
ctn_button_color = 'LightPink'

#資料顯示設定
Data_BG = "#FFFFFF"
Data_color = "000000"
total_tree_BG = "#000000"
selected_color = 'Pink'

#menu設計
menu_btn_color = "#FFFFFF"
menu_btn_width = 120
menu_btn_height = 35
menu_font_size = 20

#training size設定
T_options = [
    0.6,
    0.7,
    0.75,
    0.8,
    0.85,
    0.9
]

#Model Type
Models  = ["Linear", "SVR", "Random Forest", "AdaBoost"]

"""
notes:

tree_style = ttk.Style()
tree_style.theme_use('clam')
tree_style.configure("Treeview",
    background = setting.Data_BG,
    foreground = setting.Data_color,
    fieldbackground = setting.Data_BG
    )
tree_style.map("Treeview",
    background = [("selected", setting.selected_color)]
    )

#Tree_Frame = tk.Frame(input_frame_right, bg = setting.right_side_color, height = 600-setting.menu_height-20, width = 800-setting.left_side_width-20)
#Tree_Frame.place(x = setting.left_side_width+10, y = setting.menu_height+10)
"""