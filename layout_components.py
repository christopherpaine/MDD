import dash_daq as daq

def get_slider(df):
    return daq.Slider(
        min=df['Age x'].min(), 
        max=df['Age x'].max(), 
        value=30,
        marks={'25': 'mark', '50': '50'},
        handleLabel='Age',
        step = 1,
        id='slider-1'  # give the slider an ID
    )
