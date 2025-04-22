import pandas as pd
import plotly.express as px

def finance_line(df, start_date = '2020-01-01', end_date = '2025-01-01', tickers=['AAPL']):
    dft = (
        df
        .loc[df['Ticker'].isin(tickers)]
        .loc[df['Date'] >= start_date]
        .loc[df['Date'] <= end_date]
        )
    fig = px.line(
        dft, 
        x='Date', 
        y='Close', 
        color='Ticker', 
        color_discrete_sequence=[
            '#04af43',
            '#000000',
            '#565656',
            '#7ed4a6',
        ],
        category_orders=dict(
            Ticker=sorted(tickers)
        ),
        line_dash='Ticker',
        line_dash_sequence=[
            'solid',
            'dot',
            'solid',
            'dot',
        ],
        hover_data=dict(
            Ticker=True,
            Date=False,
            Close=True
        ),
        custom_data=['Ticker', 'Date', 'Close']
    )
    fig.update_layout(
        title_x=0.5, 
        title_y=0.95, 
        title_font=dict(size=20),
        xaxis = dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204,204,204)',
            linewidth=2,
            ticks='outside',
            tickcolor='rgb(204,204,204)',
            tickfont=dict(
                family='Montserrat, sans-serif',
                size=12,
                color='rgb(82,82,82)'
            )
        ),
        yaxis = dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204,204,204)',
            linewidth=2,
            tickfont=dict(
                family='Montserrat, sans-serif',
                size=12,
                color='rgb(82,82,82)'
            ),
        ),

        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(25,211,66,0.2)',
            font_size=11,
            font_family='Montserrat, sans-serif'
        ),
        legend=dict(
            title_text='Tickers',
            font=dict(
                family='Montserrat, sans-serif',
                size=12,
                color='rgb(82,82,82)'
            ),
            orientation='h',
            yanchor='top',
            y=1.15,
            xanchor='left',
            x=0.01,
            entrywidthmode='fraction',
            entrywidth=0.15,
        ),
        margin=dict(
            l=50, 
            r=50, 
            t=20, 
            b=50, 
            pad=4
        ),
        hovermode='x unified',
        hoverdistance=100,
        plot_bgcolor='rgba(255,255,255,0.95)'
    )

    fig.update_traces(
        line=dict(width=2), 
        marker=dict(size=4),

        hovertemplate=
            '%{customdata[0]}<br>' +
            'US$ %{y:.2f}<extra></extra>',
        )
    fig.update_xaxes(
        title_text='', 
        title_font=dict(size=16),

        showspikes=True,
        spikecolor='rgba(0,0,0,0.5)',
        spikethickness=1,
        spikemode='across',
        spikesnap='cursor',
    ),
    fig.update_yaxes(title_text='Price', title_font=dict(size=16))
    # fig.show(config={'displayModeBar': False})

    return fig


def multiple_line_chart(df, x, y, tickers):
    dft = (
        df
        .loc[df['Ticker'].isin(tickers)]
        .loc[df['Date'] >= '2025-01-01']
        )
    fig = px.line(
        dft, 
        x=x, 
        y=y, 
        color='Ticker', 
        color_discrete_sequence=[
            '#04af43',
            '#000000',
            '#565656',
            '#7ed4a6',
        ],
        category_orders=dict(
            Ticker=sorted(tickers)
        ),
        line_dash='Ticker',
        line_dash_sequence=[
            'solid',
            'dot',
            'solid',
            'dot',
        ],
        hover_data=dict(
            Ticker=True,
            Date=False,
            Close=True
        ),
        custom_data=['Ticker', 'Date', 'Close']
    )
    fig.update_layout(
        title_x=0.5, 
        title_y=0.95, 
        title_font=dict(size=20),
        xaxis = dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204,204,204)',
            linewidth=2,
            ticks='outside',
            tickcolor='rgb(204,204,204)',
            tickfont=dict(
                family='Montserrat, sans-serif',
                size=12,
                color='rgb(82,82,82)'
            )
        ),
        yaxis = dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204,204,204)',
            linewidth=2,
            tickfont=dict(
                family='Montserrat, sans-serif',
                size=12,
                color='rgb(82,82,82)'
            ),
        ),

        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(25,211,66,0.2)',
            font_size=12,
            font_family='Montserrat, sans-serif'
        ),
        legend=dict(
            title_text='Tickers',
            font=dict(
                family='Montserrat, sans-serif',
                size=12,
                color='rgb(82,82,82)'
            ),
            orientation='h',
            yanchor='top',
            y=1.1,
            xanchor='left',
            x=0.01,
            entrywidthmode='fraction',
            entrywidth=0.15,
        ),
        margin=dict(
            l=50, 
            r=50, 
            t=20, 
            b=50, 
            pad=4
        ),
        hovermode='x unified',
        hoverdistance=100,
        plot_bgcolor='rgba(255,255,255,0.95)'
    )

    fig.update_traces(
        line=dict(width=2), 
        marker=dict(size=4),

        hovertemplate=
            '%{customdata[0]}<br>' +
            'US$ %{y:.2f}<extra></extra>',
        )
    fig.update_xaxes(
        title_text=x, 
        title_font=dict(size=16),

        showspikes=True,
        spikecolor='rgba(0,0,0,0.5)',
        spikethickness=1,
        spikemode='across',
        spikesnap='cursor',
    ),
    fig.update_yaxes(title_text=y, title_font=dict(size=16))
    # fig.show(config={'displayModeBar': False})

    return fig