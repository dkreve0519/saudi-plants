import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 创建 Dash 应用
app = dash.Dash(__name__)

# 加载 Excel 数据
file_path = "Asir.xlsx"
df = pd.read_excel(file_path)

# 创建 3D 散点图，确保 custom_data 包含所有需要的信息
fig = px.scatter_3d(
    df,
    x="Soil-axis",
    y="Climate-axis",
    z="Elevation-axis",
    color="Significance",
    symbol="Plant Type",
    size="Significance count",
    hover_data=["Species"],
    custom_data=["Photo route", "Species"]  # 包含图片路径和 Species
)

# 图表布局设置
fig.update_layout(
    scene=dict(
        xaxis_title="Soil Type<br>0: Salty | 1: Sandy | 2: Rocky | 3: Loamy Soil",
        yaxis_title="Climate<br>1: Arid | 2: Semi-Arid | 3: Sub-Humid",
        zaxis_title="Elevation<br>1: Lowland | 2: Mid-altitude | 3: Highland"
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Dash 应用布局
app.layout = html.Div([
    dcc.Graph(
        id='3d-scatter-plot',
        figure=fig
    ),
    html.Div(
        id='tooltip-container',
        style={
            'position': 'absolute',
            'padding': '10px',
            'border': '1px solid gray',
            'borderRadius': '5px',
            'background': 'white',
            'visibility': 'hidden',
            'bottom': '50px',  # 设置位置为下方
            'left': '50%',    # 水平居中
            'transform': 'translateX(-50%)'  # 调整 Tooltip 居中对齐
        }
    )
], style={'position': 'relative', 'height': '100vh'})

# 悬浮时更新 Tooltip
@app.callback(
    [Output('tooltip-container', 'children'),
     Output('tooltip-container', 'style')],
    Input('3d-scatter-plot', 'hoverData')
)
def update_tooltip(hover_data):
    if hover_data is None:
        return None, {'visibility': 'hidden'}

    # 从 hover_data 中提取 customdata
    customdata = hover_data['points'][0]['customdata']
    photo_url = customdata[0]  # 图片链接
    species = customdata[1]    # 植物名称

    # 设置 Tooltip 样式
    style = {
        'position': 'absolute',
        'padding': '10px',
        'border': '1px solid gray',
        'borderRadius': '5px',
        'background': 'white',
        'visibility': 'visible',
        'bottom': '50px',  # 调整到下方
        'left': '50%',    # 水平居中
        'transform': 'translateX(-50%)'  # 居中对齐
    }

    content = html.Div(
        children=[
            html.Img(
                src=photo_url,
                style={
                    'width': '200px', 
                    'height': '200px',
                    'object-fit': 'cover',  # 防止拉伸，保持图片比例
                    'borderRadius': '5px'  # 可选：添加圆角
                }
            ),
            html.P(f"Species: {species}")
        ]
    )

    return content, style

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)
