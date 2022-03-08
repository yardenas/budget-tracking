import datetime

import dash_daq as daq
import pandas as pd
from dash import Dash, html

import figures as figs

app = Dash(__name__, title='Financial Planning and Monitoring')

budget = pd.DataFrame({
    'items': [
        'House', 'Health', 'Groceries', 'Transportation', 'Investing', 'Income',
        'Travel'
    ],
    'amounts': list(range(7))
})

actual = pd.DataFrame({
    'date': pd.Series(dtype='datetime64[ns]'),
    'amount': pd.Series(dtype=float),
    'description': pd.Series(dtype=str),
    'category': pd.Series(dtype=str)
})


def build_banner():
  return html.Header(
      id='header',
      children=[
          html.H1(datetime.datetime.now().strftime("%B") + ' Finance Dashboard')
      ])


def build_quick_stats_panel():
  return html.Div(
      id='quick-stats',
      className='panel',
      children=[
          html.Div(id='monthly-balance', children=[html.P('Monthly Balance')]),
          daq.Gauge(
              id="progress-gauge",
              max=300,
              min=0,
              showCurrentValue=True,  # default size 200 pixel
          )
      ])


def build_plan_vs_actual_panel():
  return html.Div(
      id='plan-vs-actual',
      className='panel',
      children=[
          html.H3('Budgetary Items Planned vs. Actual'),
          figs.plan_vs_actual_fig(budget)
      ])


def build_piechart():
  return html.Div(
      id='piechart-panel',
      className='panel',
      children=[
          html.H3('Budgetary Items Distribution'),
          figs.piechart(budget['items'], budget['amounts'])
      ])


app.layout = html.Div(
    id='app-container',
    children=[
        build_banner(),
        html.Div(
            className='panels',
            children=[build_plan_vs_actual_panel(),
                      build_piechart()])
    ])

if __name__ == '__main__':
  app.run_server(debug=True)
