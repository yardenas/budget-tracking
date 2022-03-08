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
          html.H3('Monthly Balance: {}'.format(23)),
          html.Div(
              id='stats',
              children=[
                  daq.Gauge(
                      id="progress-gauge",
                      size=100,
                      value=(23 / 123) * 100.0,
                      max=100,
                      min=0),
                  html.Span('Already spent: {}'.format(100), id='spent-stat'),
                  html.Span('Planned income: {}'.format(123), id='income-stat')
              ])
      ])


def build_plan_vs_actual_panel():
  return html.Div(
      id='plan-vs-actual',
      className='panel',
      children=[
          html.H4('Budgetary Items Planned vs. Actual'),
          figs.plan_vs_actual_fig(budget)
      ])


def build_piechart():
  return html.Div(
      id='piechart-panel',
      className='panel',
      children=[
          html.H4('Budgetary Items Distribution'),
          figs.piechart(budget['items'], budget['amounts'])
      ])


app.layout = html.Div(
    id='app-container',
    children=[
        build_banner(),
        build_quick_stats_panel(),
        html.Div(
            className='panels',
            children=[build_plan_vs_actual_panel(),
                      build_piechart()])
    ])

if __name__ == '__main__':
  app.run_server(debug=True)
