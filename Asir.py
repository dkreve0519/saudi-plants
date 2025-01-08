import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os

# 创建 Dash 应用并添加 meta_tags 适配移动端
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

# 加载 Excel 数据
file_path = "Asir.xlsx"
df = pd.read_excel(file_path)

# 创建 3D 散点图
fig = px.scatter_3d(
    df,
    x="Soil-axis",
    y="Climate-axis",
    z="Elevation-axis",
    color="Significance",
    symbol="Plant Type",
    size="Significance count",
    hover_data=["Species"],  # 仅保留物种名称
    custom_data=["Photo route", "Species"]  # 包含图片路径和 Species
)

# 图表布局设置，调整图例为竖向
fig.update_layout(
    scene=dict(
        xaxis_title="Soil Type<br>0: Salty | 1: Sandy | 2: Rocky | 3: Loamy Soil",
        yaxis_title="Climate<br>1: Arid | 2: Semi-Arid | 3: Sub-Humid",
        zaxis_title="Elevation<br>1: Lowland | 2: Mid-altitude | 3: Highland"
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    legend=dict(
        x=1,  # 图例靠右
        y=1,  # 图例顶部对齐
        orientation="v",  # 竖直显示图例
        xanchor="left",
        yanchor="top"
    )
)

# Dash 应用布局
app.layout = html.Div([
    dcc.Graph(
        id='3d-scatter-plot',
        figure=fig,
        style={'width': '100%', 'height': '75vh'}  # 自适应屏幕
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
            'max-width': '300px',
            'word-wrap': 'break-word',
            'bottom': '10px',  # Tooltip 在右下方显示
            'right': '10px',  # 靠右对齐
        }
    )
], style={'position': 'relative', 'height': '100vh'})

# 回调函数，处理 Hover 和隐藏
@app.callback(
    [Output('tooltip-container', 'children'),
     Output('tooltip-container', 'style')],
    Input('3d-scatter-plot', 'hoverData')
)
def update_tooltip(hover_data):
    if hover_data is None:
        # 隐藏 Tooltip
        return None, {'visibility': 'hidden'}

    # 如果 Hover 中包含数据
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
        'max-width': '300px',
        'word-wrap': 'break-word',
        'bottom': '10px',
        'right': '10px',  # 靠右下对齐
    }

    content = html.Div(
        children=[
            html.Img(
                src=photo_url,
                style={
                    'width': '200px', 
                    'height': '200px',
                    'object-fit': 'cover',
                    'borderRadius': '5px'
                }
            ),
            html.P(f"Species: {species}")
        ]
    )

    return content, style

# 获取环境变量中的端口号（Render 需要）
port = int(os.environ.get("PORT", 8050))

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=port)
